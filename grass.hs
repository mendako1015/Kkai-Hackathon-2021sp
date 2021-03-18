import Data.Char
import System.IO
import System.Environment
import Text.ParserCombinators.Parsec

data Instruction = App (Int, Int) | Abs(Int, [Instruction]) deriving Show
data Code = C [Instruction] | Out | Succ | Char Char | In deriving Show
data Function = F (Code, Environment) deriving Show
type Environment = [Function]
type Dump = Environment
type Stream = (String, String)

e0 :: Environment
e0 = [F (Out, []), F (Succ, []), F (Char 'w', []), F (In,[])]

d0 :: Dump
d0 = [F (C [App (1, 1)], []), F (C [], [])]

eval :: (Code, Environment, Dump, Stream) -> (Code, Environment, Dump, Stream)
eval (C (App (m,n) : c), e, d, s) = (cm, F (cn,en) : em, F (C c,e) : d, s)
    where F (cm,em) = e !! (m-1)
          F (cn,en) = e !! (n-1)
eval (C (Abs (1,c') : c), e, d, s) = (C c, F (C c',e) : e, d, s)
eval (C (Abs (n,c') : c), e, d, s) = (C c, F (C [Abs (n-1,c')], e) : e, d, s)
eval (C [], f : e, F (c',e') : d, s) = (c', f : e', d, s)
eval (Out, f@(F (Char c,_)) : e, d, (o,i)) = (C [], f : f : e, d, (c:o,i))
eval (Out, F (c',f) : _, _, _) = error $ "Not a character: " ++ show c'
eval (In, f : e, d, (o,[])) = (C [], f : e, d, (o,[]))
eval (In, e, d, (o,c:i)) = (C [], F (Char c,[]) : e, d, (o,i))
eval (Succ, f@(F (Char c,_)) : e, d, s) =
    (C [], F (Char (chr $ mod (ord c + 1) 256),[]) : f : e, d, s)
eval (Succ, F (c',f) : _, _, _) = error $ "Not a character: " ++ show c'
eval (Char c0, f@(F (Char c1,_)) : e, d, s) =
    (if c0==c1 then C [Abs (1,[]), Abs (2,[App (3,2)])] else C [Abs (2,[])], f : e, d, s)
eval (Char _, e, d, s) = (C [Abs (2,[])], e, d, s)

notTerm :: (Code, Environment, Dump, Stream) -> Bool
notTerm (C [], _, [], _) = False
notTerm _ = True

run :: Code -> String -> String
run c0 i = out $ head $ dropWhile notTerm $ iterate eval(c0, e0, d0, ([], i))
    where
        out (_, _, _, (o, _)) = reverse o

chars :: Char -> Parser Int
chars c = length <$> many1 (char c)

app :: Parser Instruction
app = do
    u <- chars 'W'
    l <- chars 'w'
    return $ App (u, l)

abst :: Parser Instruction
abst = do
    l <- chars 'w'
    a <- many app
    return $ Abs (l, a)

prog :: Parser [Instruction]
prog =  try (do
        a <- abst
        eof
        return [a])
    <|> try (do
        a <- abst
        v <- char 'v'
        ap <- many app
        eof
        return $ a:ap)
    <|> do
        a <- abst
        v <- char 'v'
        p <- prog
        return $ a:p

filter' :: String -> String
filter' [] = []
filter' ('W':s) = 'W' : filter' s
filter' ('v':s) = 'v' : filter' s
filter' ('w':s) = 'w' : filter' s
filter' ('\xef':'\xbc':'\xb7':s) = 'W' : filter' s
filter' ('\xef':'\xbd':'\x96':s) = 'v' : filter' s
filter' ('\xef':'\xbd':'\x97':s) = 'w' : filter' s
filter' ('\x82':'\x76':s) = 'W' : filter' s
filter' ('\x82':'\x96':s) = 'v' : filter' s
filter' ('\x82':'\x97':s) = 'w' : filter' s
filter' (_:s) = filter' s

parseProg :: String -> Code
parseProg s = 
    case parse prog "" $ dropWhile (/= 'w') $ filter' s of
        Right  i -> C i
        Left err -> error $ show err

main :: IO ()
main = interact . run . parseProg =<< readFile . head =<< getArgs