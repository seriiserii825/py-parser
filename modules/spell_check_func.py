from classes.SpellCheck import SpellCheck


def spell_check_func(soup):
    sp = SpellCheck()
    sp.spell_check(soup)
