from django import template

register = template.Library()

@register.filter
def make_star(value):
    """
    Custom filter to convert numeric rating to star symbols.
    """
    stars = "★" * int(value)
    return stars


@register.filter
def times(number):
    """
    Custom filter to generate a range of numbers from 1 to the given number.
    """
    return range(1, number + 1)

@register.filter
def is_string(value):
    """
    Custom template filter to check if the value is a string.
    """
    return isinstance(value, str)


@register.filter
def extract_first_letter(nickname):
    return nickname[0]
