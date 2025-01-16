import pygame

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from bottom import Bootom
from game_status import Gamestatus
from scoreboard import Scoreboard
import game_fuctions as gf

def run_game():
    '''初始化游戏并创建对象'''
    pygame.init()
    pygame.display.set_caption("Alien Invasion")

    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    stats=Gamestatus(ai_settings)
    ship=Ship(ai_settings,screen)
    alien=Alien(ai_settings,screen)
    sb=Scoreboard(ai_settings,screen,stats)
    aliens=Group()
    bullets=Group()

    gf.creat_fleet(ai_settings,screen,ship,aliens)
    play_button=Bootom(ai_settings,screen,"Play")
    '''开始主循环'''
    while True:
        gf.chek_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullet(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button)

        

run_game()