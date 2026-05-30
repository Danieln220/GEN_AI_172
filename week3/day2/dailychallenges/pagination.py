import math


class Pagination:
    def __init__(self, items=None, page_size=10):
        self.items = items if items is not None else []
        self.page_size = page_size
        self.current_idx = 0
        self.total_pages = math.ceil(len(self.items) / self.page_size) if self.items else 0

    def get_visible_items(self):
        start = self.current_idx * self.page_size
        end = start + self.page_size
        return self.items[start:end]

    def go_to_page(self, page_num):
        if page_num < 1 or page_num > self.total_pages:
            raise ValueError(
                f"Page {page_num} is out of range. Valid pages are 1 to {self.total_pages}."
            )
        self.current_idx = page_num - 1
        return self

    def first_page(self):
        self.current_idx = 0
        return self

    def last_page(self):
        self.current_idx = self.total_pages - 1
        return self

    def next_page(self):
        if self.current_idx < self.total_pages - 1:
            self.current_idx += 1
        return self

    def previous_page(self):
        if self.current_idx > 0:
            self.current_idx -= 1
        return self

    def __str__(self):
        return "\n".join(str(item) for item in self.get_visible_items())


# ── Tests ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    alphabetList = list("abcdefghijklmnopqrstuvwxyz")
    p = Pagination(alphabetList, 4)

    # __str__ bonus
    print("str(p):")
    print(str(p))
    print()

    # get_visible_items on page 1
    print("get_visible_items() on page 1:")
    print(p.get_visible_items())  # ['a', 'b', 'c', 'd']

    # next_page then get_visible_items
    p.next_page()
    print("\nAfter next_page():")
    print(p.get_visible_items())  # ['e', 'f', 'g', 'h']

    # last_page then get_visible_items
    p.last_page()
    print("\nAfter last_page():")
    print(p.get_visible_items())  # ['y', 'z']

    # go_to_page out of range (>= total pages)
    print("\ngo_to_page(10) — expecting ValueError:")
    try:
        p.go_to_page(10)
    except ValueError as e:
        print(f"ValueError: {e}")

    # go_to_page(0) — pages are 1-based, so 0 is invalid
    print("\ngo_to_page(0) — expecting ValueError:")
    try:
        p.go_to_page(0)
    except ValueError as e:
        print(f"ValueError: {e}")

    # Bonus: method chaining
    p.first_page()
    print("\nMethod chaining — p.next_page().next_page().next_page().get_visible_items():")
    print(p.next_page().next_page().next_page().get_visible_items())  # ['m', 'n', 'o', 'p']
