'''
Printing utils

Main uses:
  print_match("WORDS", 242, nl=True) -> Print word with (numeric) pattern
  print_simple_match(123, nl=True) -> Print pattern
'''
import collections
import math

# Pattern constants
MISS = 0
MISPLACED = 1
EXACT = 2

class ColorPrint:
  RED = '\033[91m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  END = '\033[0m'

  @classmethod
  def cp(self, color, s, **kwargs):
    print(color + s + self.END, **kwargs),

  @classmethod
  def r(self, s, **kwargs):
    self.cp(self.RED, s, **kwargs)

  @classmethod
  def g(self, s, **kwargs):
    self.cp(self.GREEN, s, **kwargs)

  @classmethod
  def y(self, s, **kwargs):
    self.cp(self.YELLOW, s, **kwargs)

  @classmethod
  def tc(self, s, match):
    if match == EXACT:
      self.g(s, end='')
    elif match == MISPLACED:
      self.y(s, end='')
    elif match == MISS:
      self.r(s, end='')

  @classmethod
  def simple(self, match):
    if match == EXACT:
      self.g('O', end='')
    elif match == MISPLACED:
      self.y('?', end='')
    elif match == MISS:
      self.r('-', end='')

def p2a(pattern):
  a = [0]*5
  i = 4
  while i >= 0:
    a[i] = pattern%3
    pattern = pattern//3
    i -= 1
  return a

def a2p(array):
  p = 0
  for match in array:
    p = 3*p + match
  return p

def a2s(array):
  str_pat = ""
  for match in array:
    if match == EXACT:
      str_pat += 'O'
    elif match == MISPLACED:
      str_pat += '?'
    elif match == MISS:
      str_pat += '-'
  return str_pat

def p2s(pattern):
  a = p2a(pattern)
  return a2s(a)

def print_match(word, pattern, nl=True):
  colors = p2a(pattern)
  for i, c in enumerate(word):
    ColorPrint.tc(c, colors[i])
  if nl:
    print("")

def print_simple_match(pattern, nl=True):
  colors = p2a(pattern)
  for i in range(5):
    ColorPrint.simple(colors[i])
  print(" (%3d)" % pattern, end="")
  if nl:
    print("")
    
def test_match(guess, secret):
  guess = list(guess)
  secret = list(secret)
  match = [MISS]*5
  for i in range(5):
    if(guess[i] == secret[i]):
      match[i] = EXACT
      guess[i] = '_'
      secret[i] = '@'
  for i in range(5):
    for j in range(5):
      if(guess[i] == secret[j]):
        match[i] = MISPLACED
        guess[i] = '_'
        secret[j] = '@'
  return a2p(match)

def test_matches(w1, w2):
  w1 = list(w1)
  w2 = list(w2)
  m1 = [MISS]*5
  m2 = [MISS]*5
  for i in range(5):
    if w1[i] == w2[i]:
      m1[i] = m2[i] = EXACT
      w1[i] = '_'
      w2[i] = '@'
  for i in range(5):
    for j in range(5):
      if w1[i] == w2[j]:
        m1[i] = m2[j] = MISPLACED
        w1[i] = '_'
        w2[j] = '@'
  return a2p(m1), a2p(m2)

def get_freqs(guess, words, all_pat=None, warn_every=0):
  p_count = collections.defaultdict(int)
  if all_pat:
    for i, word in enumerate(words):
        if warn_every > 0 and (i % warn_every == 0):
            print(i) 
        p = all_pat[guess][word]
        p_count[p] += 1
  else:
    for i, word in enumerate(words):
      if warn_every > 0 and (i % warn_every == 0):
        print(i)
      p = test_match(guess, word)
      p_count[p] += 1
  return p_count
    
def get_all_freqs(words, warn_every=0):
  all_patterns = collections.defaultdict(dict)
  full_match = a2p([EXACT]*5)
  for i in range(len(words)):
    if warn_every > 0 and i % warn_every == 0:
        print("%4d" % i, words[i])
    all_patterns[words[i]][words[i]] = full_match
    for j in range(i, len(words)):
      p_ij, p_ji = test_matches(words[i], words[j])
      all_patterns[words[i]][words[j]] = p_ij
      all_patterns[words[j]][words[i]] = p_ji
  return all_patterns

def compute_entropy(freqs, size):
  e = 0.0
  for pattern, count in freqs.items():
    p = count/size
    e += p * math.log2(1/p)
  return e

def filter_list(words, guess, patt, a_p):
    # could be a lambda
    filtered_list = []
    for word in words:
        if a_p[guess][word] == patt:
            filtered_list.append(word)
    return filtered_list
