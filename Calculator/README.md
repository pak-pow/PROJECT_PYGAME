# 🧮 Pygame Calculator

A fully functional GUI calculator built from scratch using **Pygame**. 

While Pygame is typically used for games, this project serves as a foundational exercise in **UI Development**. It focuses on detecting mouse clicks, mapping coordinates to buttons, and managing internal state logic without relying on standard GUI toolkits like Tkinter.

## ✨ Features

* **Arithmetic Operations:** Supports Addition, Subtraction, Multiplication, and Division.
* **Custom UI:** Buttons and display area drawn entirely using Pygame `Rect` objects.
* **Mouse Handling:** Detects clicks mapped to a grid layout.
* **Error Safety:** Handles basic errors (like Division by Zero) gracefully.

## 🧠 Key Concepts Learned

* **Event Handling:** Differentiating between `MOUSEBUTTONDOWN` and other events.
* **Coordinate Mapping:** checking if `mouse_pos` collides with button rectangles (`collidepoint`).
* **State Management:** Storing the current number, the operator, and the result in variables.
* **Text Rendering:** Using `pygame.font` to render dynamic numbers to the screen.

## 🚀 How to Run

1.  **Navigate to the calculator directory:**
    ```bash
    cd Calculator
    ```

2.  **Run the script:**
    ```bash
    python main.py
    ```

## 🎮 Controls

* **Left Click:** Interact with buttons.
* **C Button:** Clear the current entry/result.
