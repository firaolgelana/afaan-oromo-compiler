import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from src.lexer.lexer import Lexer
from src.errors.diagnostics import Diagnostics

src = Path("test_p1.ao").read_text(encoding="utf-8")
lexer = Lexer(src, Diagnostics())
tokens = lexer.tokenize()
for t in tokens:
    print(t)
