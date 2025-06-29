import random
import uuid

ADJECTIVES = [
    "silent", "fuzzy", "tiny", "wild", "sleepy", "noisy", "brave", "elegant", "mighty", "zesty",
    "shiny", "weird", "bright", "slow", "quick", "lazy", "funny", "grumpy", "loopy", "snappy",
    "cranky", "fancy", "nimble", "silly", "charming", "bouncy", "quirky", "jazzy", "dreamy", "witty",
    "zany", "crafty", "dizzy", "jolly", "plucky", "spunky", "wobbly", "spicy", "clumsy", "frisky"
]

NAMES = [
    "turing", "curie", "lovelace", "einstein", "fermat", "newton", "hopper", "bohr", "planck",
    "darwin", "pasteur", "tesla", "gauss", "galilei", "archimedes", "feynman", "kepler", "dirac",
    "leonardo", "copernicus", "berners", "torvalds", "musk", "godel", "bernoulli", "noether",
    "mandelbrot", "heisenberg", "babbage", "knuth", "von_neumann", "da_vinci", "ada", "euclid",
    "euler", "marconi", "volta", "ohm", "boole"
]

def generate_random_holder_name():
    return f"{random.choice(ADJECTIVES)}_{random.choice(NAMES)}_{uuid.uuid4().hex[:5]}"