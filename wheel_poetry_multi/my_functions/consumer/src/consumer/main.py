from mymath import add_two_numbers, multiply_two_numbers

def compute_sum_and_product(a, b):
    sum_val = add_two_numbers(a, b)
    prod_val = multiply_two_numbers(a, b)
    return sum_val, prod_val

def combined_output(a, b):
    sum_val, prod_val = compute_sum_and_product(a, b)
    return f"Sum is {sum_val} and product is {prod_val}"


__all__ = ["combined_output", "compute_sum_and_product"]