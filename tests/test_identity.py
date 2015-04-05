"""
Tests for the Identity Monad.

Functor laws:
    * http://learnyouahaskell.com/functors-applicative-functors-and-monoids

Applicative laws:
    * http://en.wikibooks.org/wiki/Haskell/Applicative_Functors

Monad laws:
    * http://learnyouahaskell.com/a-fistful-of-monads#monad-laws
    * https://wiki.haskell.org/Monad_laws
"""
import unittest

from oslash.identity import Identity
from oslash.util import identity, compose, compose2

pure = Identity.pure
return_ = Identity.return_


class TestIdentityFunctor(unittest.TestCase):

    def test_identity_functor_fmap(self):
        x = return_(42)
        f = lambda x: x * 10

        self.assertEqual(
            x.fmap(f),
            return_(420)
        )

    def test_identity_functor_law_1(self):
        # fmap id = id
        x = return_(42)

        self.assertEqual(
            x.fmap(identity),
            x
        )

    def test_identity_functor_law2(self):
        # fmap (f . g) x = fmap f (fmap g x)
        def f(x):
            return x+10

        def g(x):
            return x*10

        x = return_(42)

        self.assertEquals(
            x.fmap(compose(f, g)),
            x.fmap(g).fmap(f)
        )


class TestIdentityApplicative(unittest.TestCase):

    def test_identity_applicative_law_functor(self):
        # pure f <*> x = fmap f x
        x = return_(42)
        f = lambda x: x * 42

        self.assertEquals(
            pure(f).apply(x),
            x.fmap(f)
        )

    def test_identity_applicative_law_identity(self):
        # pure id <*> v = v
        v = return_(42)

        self.assertEquals(
            pure(identity).apply(v),
            v
        )

    def test_identity_applicative_law_composition(self):
        # pure (.) <*> u <*> v <*> w = u <*> (v <*> w)

        w = return_(42)
        u = pure(lambda x: x * 42)
        v = pure(lambda x: x + 42)

        self.assertEquals(
            pure(compose2).apply(u).apply(v).apply(w),
            u.apply(v.apply(w))
        )

    def test_identity_applicative_law_homomorphism(self):
        # pure f <*> pure x = pure (f x)
        x = 42
        f = lambda x: x * 42

        self.assertEquals(
            pure(f).apply(pure(x)),
            pure(f(x))
        )

    def test_identity_applicative_law_interchange(self):
        # u <*> pure y = pure ($ y) <*> u

        y = 43
        u = return_(lambda x: x*42)

        self.assertEquals(
            u.apply(pure(y)),
            pure(lambda f: f(y)).apply(u)
        )


class TestIdentityMonad(unittest.TestCase):

    def test_identity_monad_bind(self):
        m = return_(42)
        f = lambda x: return_(x*10)

        self.assertEqual(
            m.bind(f),
            return_(420)
        )

    def test_identity_monad_law_left_identity(self):
        # return x >>= f is the same thing as f x

        f = lambda x: return_(x+100000)
        x = 3

        self.assertEqual(
            return_(x).bind(f),
            f(x)
        )

    def test_identity_monad_law_right_identity(self):
        # m >>= return is no different than just m.

        m = return_("move on up")

        self.assertEqual(
            m.bind(return_),
            m
        )

    def test_identity_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        m = return_(42)
        f = lambda x: return_(x+1000)
        g = lambda y: return_(y*42)

        self.assertEqual(
            m.bind(f).bind(g),
            m.bind(lambda x: f(x).bind(g))
        )