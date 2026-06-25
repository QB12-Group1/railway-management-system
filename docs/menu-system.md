## Reusable Menu Helpers

The shared menu helpers live in `app/menus/base.py`.

### `handle_options`

Use `handle_options()` when a menu only needs to show a numbered list and call
an action based on the selected option.

Example:

```python
class ExampleMenu(BaseMenu):
    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Example Menu",
            {
                "Say hello": lambda controller: print("Hello!"),
                "Go back": lambda controller: controller.pop(),
            },
        )
```

This avoids repeating the same pattern in every menu:

- show title
- show numbered options
- read user input
- validate selected number
- call the selected action

### `get_required_feedback`

Use `get_required_feedback()` when a field cannot be empty.

Example:

```python
username = self.get_required_feedback("Username: ")
password = self.get_required_feedback("Password: ")
```

If the user submits an empty value, the helper prints the invalid input message
and asks again.

### `pause`

Use `pause()` when you want the user to read output before the next menu render.

Example:

```python
print("Staff member added successfully.")
self.pause()
```

## Adding New Menus

For simple menus, create a new class that extends `BaseMenu` and call
`handle_options()` from `display()`.

```python
class AdminMenu(BaseMenu):
    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Admin Menu",
            {
                "Add staff": self.add_staff,
                "Back": lambda controller: controller.pop(),
            },
        )

    def add_staff(self, controller: MenuController) -> None:
        username = self.get_required_feedback("Username: ")
        print(f"Adding staff user {username}.")
```

This keeps future menus smaller and makes their options easier to read.
