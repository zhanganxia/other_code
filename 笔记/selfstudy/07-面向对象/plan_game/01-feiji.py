import pygame
from pygame.locals import *
    

# 创建玩家的飞机类
class PlayerPlan(object):
    # 初始化方法，飞机的默认设置
    def __init__(self,screen):
        # 存储子弹列表
        self.bulletList = []

        # 飞机图片
        planeImageName = './images/life.png'
        self.image = pygame.image.load(planeImageName)

        # 设置默认的坐标(左上角为(0,0))
        self.x = 230
        self.y = 600
        self.screen = screen

        # 设置速度
        self.speed = 5

        # 设置飞机的名字
        self.planeName = 'player'

        # 
    
    # 将飞机显示出来
    def draw(self):
        self.screen.blit(self.image,(self.x,self.y))

    def keyHandle(self,keyValue):
        if keyValue == 'left':
            print('--按下  左键--')
            self.x -= 20
        if keyValue == 'right':
            print('--按下  右键--')
            self.x += 20
        if keyValue == 'space':
            print('--按下  空格键--')
        
        # self.draw()

if __name__ == '__main__':
    screen = pygame.display.set_mode((480,890),0,32)

    bgImageFile = './images/background.png'
    background = pygame.image.load(bgImageFile).convert()

    player = PlayerPlan(screen)
    # 1.显示背景
    # screen.blit(background,(0,0))
    # pygame.display.update()
    # 2.步骤1显示的背景 一闪而过
    while True:
        screen.blit(background,(0,0))

        # 判断是否是点击了退出按钮  检测键盘
        for event in pygame.event.get():
            if event.type == QUIT:
                print('exit')
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    player.keyHandle('left')

                elif event.key == K_d or event.key == K_RIGHT:
                    player.keyHandle('right')


                elif event.key == K_SPACE:
                    print('space')
        
        player.draw()
        pygame.display.update()