# +========================+
# | ERROR HANDELING custom |
# +========================+

try:
    # Code that might raise an exception
    print("Enter your code here")

# Catch any exception
except Exception as e:
    print(f"Unexpected error: {e}")

# Common Python exceptions individually
except AttributeError as e:
    print(f"AttributeError: {e}")
except TypeError as e:
    print(f"TypeError: {e}")
except ValueError as e:
    print(f"ValueError: {e}")
except IndexError as e:
    print(f"IndexError: {e}")
except KeyError as e:
    print(f"KeyError: {e}")
except NameError as e:
    print(f"NameError: {e}")
except ZeroDivisionError as e:
    print(f"ZeroDivisionError: {e}")
except FileNotFoundError as e:
    print(f"FileNotFoundError: {e}")
except IOError as e:
    print(f"IOError: {e}")
except ImportError as e:
    print(f"ImportError: {e}")
except StopIteration as e:
    print(f"StopIteration: {e}")
except AssertionError as e:
    print(f"AssertionError: {e}")
except MemoryError as e:
    print(f"MemoryError: {e}")
except OverflowError as e:
    print(f"OverflowError: {e}")