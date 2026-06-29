## Reusable Menu Helpers

The shared menu helpers live in `app/menus/base.py`.

## Cancelling Operations

Type `exit` during a menu prompt to cancel the current operation and return one
menu level back.

For example, if the app is asking for a login username or password, entering
`exit` cancels login and returns to the main menu.

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

Use `get_required_feedback()` when a field cannot be empty and should support
the shared cancel command.

Example:

```python
username = self.get_required_feedback("Username: ")
if username is None:
    self.cancel_operation(controller)
    return

password = self.get_required_feedback("Password: ")
if password is None:
    self.cancel_operation(controller)
    return
```

If the user submits an empty value, the helper prints the invalid input message
and asks again. If the user enters `exit`, the helper returns `None` so the menu
can cancel the operation.

### `pause`

Use `pause()` when you want the user to read output before the next menu render.

Example:

```python
print("Staff member added successfully.")
self.pause()
```

## `not_implemented_yet`

Use `not_implemented_yet()` as a temporary placeholder for menu options that are
planned but not implemented yet.

Example:

```python
class AdminMenu(BaseMenu):
    def display(self, controller: MenuController) -> None:
        self.handle_options(
            controller,
            "Admin Menu",
            {
                "Add staff": self.add_staff,
                "Remove staff": self.remove_staff,
                "list staff": self.not_implemented_yet, # TODO: implement viewing staffs functionallity(menu)
                "Back": lambda controller: controller.pop(),
            },
        )
```

When selected, this helper prints a message to inform the user that the feature
is not available yet, then returns one menu level back.

This is useful when:

- a menu option should appear now, but its logic will be added later
- you want unfinished features to fail in a consistent way
- you want to avoid writing duplicate placeholder code in multiple menus

If the option should remain on the same menu instead of returning back, implement
a custom placeholder action instead.

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
        if username is None:
            self.cancel_operation(controller)
            return

        print(f"Adding staff user {username}.")
```

This keeps future menus smaller and makes their options easier to read.
