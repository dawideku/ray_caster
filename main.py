import glfw
import math
from OpenGL.GL import *
from OpenGL.GLU import *

player_x = 0.0
player_y = 0.0
player_delta_x = 0.0
player_delta_y = 0.0
player_angle = 0.0


def draw_player():
    glColor3f(1.0, 1.0, 0)
    glPointSize(8.0)
    glBegin(GL_POINTS)
    glVertex2f(player_x, player_y)
    glEnd()

    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex2f(player_x, player_y)
    glVertex2f(player_x + player_delta_x * 5, player_y + player_delta_y * 5)
    glEnd()

mapx = 8
mapy = 8
maps = 64
map_tab = [
    [1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,1],
    [1,0,1,0,0,0,0,1],
    [1,0,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1],
]

def draw_2d_map():
    for i in range(mapy):
        for j in range(mapx):
            temp_x = j * maps
            temp_y = i * maps
            if map_tab[i][j] == 1:
                glColor3f(1.0, 1.0, 1.0)
            else:
                glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_QUADS)
            glVertex2f(temp_x + 1, temp_y + 1)
            glVertex2f(temp_x + 1, temp_y + maps - 1)
            glVertex2f(temp_x+maps - 1, temp_y+maps - 1)
            glVertex2f(temp_x+maps - 1, temp_y + 1)
            glEnd()

def distance(ax, bx, ay, by):
    return math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)

def draw_rays_2d():
    rays = 1
    ray_angle = player_angle
    ray_x, ray_y, x_offset, y_offset = 0.0, 0.0, 0.0, 0.0
    for i in range(rays):
        # horizontal line
        dis_horizontal = 1000000
        hor_x = player_x
        hor_y = player_y
        depth_of_field = 0
        if math.isclose(math.tan(ray_angle), 0, abs_tol=1e-10):
            inv_tan = 1e10  # Duża wartość zastępuje nieskończoność
        else:
            inv_tan = -1 / math.tan(ray_angle)
        if ray_angle > math.pi:
            ray_y = ((int(player_y) >> 6) << 6) - 0.0001
            ray_x = (player_y - ray_y) * inv_tan + player_x
            y_offset = -64
            x_offset = (-y_offset) * inv_tan
        if ray_angle < math.pi:
            ray_y = ((int(player_y) >> 6) << 6) + 64
            ray_x = (player_y - ray_y) * inv_tan + player_x
            y_offset = 64
            x_offset = (-y_offset) * inv_tan
        if ray_angle == 0 or ray_angle == math.pi:
            ray_x = player_x
            ray_y = player_y
            depth_of_field = 8
        while depth_of_field < 8:
            m_x = int(ray_x) >> 6
            m_y = int(ray_y) >> 6
            m_p = m_y * mapx + m_x
            if -1 < m_p < mapx * mapy and map_tab[int(m_p / 8)][m_p % 8] == 1:
                depth_of_field = 8
                hor_x = ray_x
                hor_y = ray_y
                dis_horizontal = distance(player_x, hor_x, player_y, hor_y)
            else:
                ray_x += x_offset
                ray_y += y_offset
                depth_of_field += 1

        #vertical line
        dis_vertical = 1000000
        ver_x = player_x
        ver_y = player_y
        depth_of_field = 0
        neg_tan = -math.tan(ray_angle)
        if 3 * math.pi / 2 > ray_angle > math.pi / 2:
            ray_x = ((int(player_x) >> 6) << 6) - 0.0001
            ray_y = (player_x - ray_x) * neg_tan + player_y
            x_offset = -64
            y_offset = (-x_offset) * neg_tan
        if ray_angle < math.pi / 2 or ray_angle > 3 * math.pi / 2:
            ray_x = ((int(player_x) >> 6) << 6) + 64
            ray_y = (player_x - ray_x) * neg_tan + player_y
            x_offset = 64
            y_offset = (-x_offset) * neg_tan
        if ray_angle == 0 or ray_angle == math.pi:
            ray_x = player_x
            ray_y = player_y
            depth_of_field = 8
        while depth_of_field < 8:
            m_x = int(ray_x) >> 6
            m_y = int(ray_y) >> 6
            m_p = m_y * mapx + m_x
            if -1 < m_p < mapx * mapy and map_tab[int(m_p / 8)][m_p % 8] == 1:
                depth_of_field = 8
                ver_x = ray_x
                ver_y = ray_y
                dis_vertical = distance(player_x, ver_x, player_y, ver_y)
            else:
                ray_x += x_offset
                ray_y += y_offset
                depth_of_field += 1
        if dis_horizontal > dis_vertical:
            ray_x = ver_x
            ray_y = ver_y
        else:
            ray_x = hor_x
            ray_y = hor_y

        glColor3f(0.0, 0.0, 1.0)
        glLineWidth(3.0)
        glBegin(GL_LINES)
        glVertex2f(player_x, player_y)
        glVertex2f(ray_x, ray_y)
        glEnd()

def key_callback(window, key, scancode, action, mods):
    global player_x, player_y, player_angle, player_delta_x, player_delta_y
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:  # Klawisz W - ruch w górę
            player_x += player_delta_x
            player_y += player_delta_y
        if key == glfw.KEY_S:  # Klawisz S - ruch w dół
            player_x -= player_delta_x
            player_y -= player_delta_y
        if key == glfw.KEY_A:  # Klawisz A - ruch w lewo
            player_angle -= 0.1
            if player_angle < 0:
                player_angle += 2 * math.pi
            player_delta_x = math.cos(player_angle) * 5
            player_delta_y = math.sin(player_angle) * 5
        if key == glfw.KEY_D:  # Klawisz D - ruch w prawo
            player_angle += 0.1
            if player_angle > 2 * math.pi:
                player_angle -= 2 * math.pi
            player_delta_x = math.cos(player_angle) * 5
            player_delta_y = math.sin(player_angle) * 5


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_2d_map()
    draw_rays_2d()
    draw_player()
    # Code for writing
    glfw.swap_buffers(window)

def init():
    global player_x, player_y, player_delta_x, player_delta_y
    glClearColor(0.3, 0.3, 0.3, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 1024, 512, 0)
    glMatrixMode(GL_MODELVIEW)
    player_x = 300.0
    player_y = 300.0
    player_delta_x = math.cos(player_angle) * 5
    player_delta_y = math.sin(player_angle) * 5

def main():
    global window

    # Initialize GLFW
    if not glfw.init():
        print("Failed to initialize GLFW")
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1024, 512, "Raycaster", None, None)
    if not window:
        glfw.terminate()
        print("Failed to create GLFW window")
        return

    # Make the window's context current
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    # Initialize OpenGL settings
    init()

    # Main render loop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        display()
        glfw.poll_events()

    # Terminate GLFW
    glfw.terminate()

if __name__ == '__main__':
    main()
