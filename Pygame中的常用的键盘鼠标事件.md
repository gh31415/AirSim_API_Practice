## Pygame中的多按键检测

#### Pygame

​    Pygame 是一个 Python 的游戏开发库，可以用于创建电子游戏。它是基于 Simple DirectMedia Layer（SDL）库封装的，提供了一系列具有跨平台性质的游戏开发 API，包括图像处理，声音，输入，事件处理等。这个库可以在 Windows、Mac OS X、Linux 和移动设备上运行。

​    Pygame 很容易上手并且非常易于使用，有很多教程和代码示例供参考。企业和个人游戏开发者在使用 Pygame 开发 2D 游戏方面，都能找到很好的支持。

Pygame 的特点包括：

- 易用性：Pygame 的 API 简单、易学、易用，使得游戏开发者可以从事游戏逻辑和即时分析。
- 多样性：Pygame 在用户输入、声音、图形处理等方面的支持广泛。
- 可扩展性：除了 Pygame 本身提供的功能外，还可以使用 Python 的其他库和工具，为开发者提供更强大的功能支持。
- 开源性：Pygame 是一种免费且开源的软件，遵循 LGPL 许可证。

### Pygame中的常用的键盘鼠标事件

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('keyboard ctrl')
screen.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        # >------>>>  处理鼠标事件   <<<------< #
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Down: ", event)
        if event.type == pygame.MOUSEBUTTONUP:
            print("Mouse Up", event)
        if event.type == pygame.MOUSEMOTION:
            print("Mouse is moving now: ", event)
            
        # >------>>>  处理键盘事件   <<<------< #
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("keyboard event: ", event)

```

​	这段代码使用 Pygame 函数库创建了一个名为 "keyboard ctrl" 的窗口，并实现了鼠标和键盘事件的处理。具体来说，它包括以下几个部分：

1. 启动 Pygame 应用程序：首先，`pygame.init()` 函数初始化 Pygame 应用程序和所需的子模块。接下来，`pygame.display.set_mode((640, 480))` 创建了一个名为 screen 的 Pygame 窗口，并设置了其大小为 640x480 像素。最后，`pygame.display.set_caption('keyboard ctrl')` 设置窗口标题为 "keyboard ctrl"。

2. `screen.fill((0, 0, 0))` 是用来填充屏幕背景颜色的。具体来说，这会将屏幕填充为黑色（RGB 为 (0,0,0)）。

   `fill()` 是 Pygame.Surface 对象的方法，用于填充指定矩形区域或整个表面。当指定背景颜色时，它会先把表面全部填充为该背景颜色，然后再进行其他绘制操作，以此实现新的显示效果。

3. 处理鼠标事件：该代码段使用 Pygame 的事件管理器，`pygame.event.get()` 函数获取所有当前的事件列表，并通过循环逐一处理每个事件。在这里，该代码段侦听了三种鼠标事件：`pygame.MOUSEBUTTONDOWN`、`pygame.MOUSEBUTTONUP` 和 `pygame.MOUSEMOTION`，分别表示鼠标按下、释放和移动的事件,并使用 `print()` 语句将每个事件打印到控制台中。

4. 处理键盘事件：该代码段还侦听了一个键盘事件 `pygame.KEYDOWN`，并将键盘事件本身作为参数传递给处理函数。如果键盘事件是回车键 `pygame.K_RETURN`，则在控制台中输出 "keyboard event: "。

5. 无限循环：最后，该代码段使用一个无限循环来保持 Pygame 应用程序处于运行状态，并在退出时释放资源。在这里，该代码段仅侦听 `pygame.QUIT` 事件以退出循环和应用程序。

### Pygame实现多按键检测

```python
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('keyboard ctrl')
screen.fill((0, 0, 0))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    scan_wrapper = pygame.key.get_pressed()
    print("pressed keys is ", scan_wrapper)
    
    # press 'Esc' to quit
    if scan_wrapper[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
```

这段代码使用了Pygame库创建了一个窗口，并且在按下键盘时打印出哪些键被按下。其中，当按下“Esc”键时，程序会退出。

首先，代码通过`pygame.init()`初始化Pygame库。然后，使用`pygame.display.set_mode()`创建了一个640x480的窗口，并设置了窗口标题为“keyboard ctrl”。接着，通过调用`screen.fill((0, 0, 0))`对窗口进行黑色填充，使得窗口背景变成黑色。

之后，代码进入了一个无限循环。在每次循环中，程序通过`pygame.event.get()`获取所有的事件，并逐个处理。

然后，使用`pygame.key.get_pressed()`检查当前哪些键被按下，将结果存储在名为`scan_wrapper`的列表中。最后，程序检查`scan_wrapper`列表中是否有`pygame.K_ESCAPE`键被按下，如果按下该键，则程序会通过调用`pygame.quit()`和`sys.exit()`来正常退出。

****

`sys.exit()`是Python内置的函数，用于退出程序。其作用是引发一个`SystemExit`异常，然后退出程序。

当调用`sys.exit()`时，会立即停止程序运行，并且不会执行该语句之后的代码。如果在主线程中调用`sys.exit()`，那么整个程序都会退出，所有子线程也会被终止。

通常情况下，在Python中正常退出程序应该使用`sys.exit()`而不是直接使用`exit()`或者`quit()`。其中，`exit()`和`quit()`是Python的内置函数，它们和`sys.exit()`类似，但是没有提供给用户设置退出状态码的选项。

需要注意的是，在大多数情况下并不建议使用`sys.exit()`来退出程序，而是应该让程序在正常流程结束后自动退出。在某些特殊场景下，比如使用系统信号来强制终止程序时，可以使用`sys.exit()`来保证程序能够正确退出。

### Pygame 多按键检测约束到（26个字母+↑↓←→键）

```python
import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('keyboard ctrl')
screen.fill((0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    for i in range(26):
        if keys[pygame.K_a + i]:  # 检测从 A 到 Z 的按键
            print(chr(pygame.K_a + i))

    # 检测上下左右键
    if keys[pygame.K_UP]:
        print("Up arrow")
    if keys[pygame.K_DOWN]:
        print("Down arrow")
    if keys[pygame.K_LEFT]:
        print("Left arrow")
    if keys[pygame.K_RIGHT]:
        print("Right arrow")

    # 按下 'Esc' 退出程序
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
```

注：当pygame的窗口界面出来后一定要将中文输入法改为英文输入法，否则会检测不到。
