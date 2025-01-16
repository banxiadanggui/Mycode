import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
def chek_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    '''监视动作'''
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
            ckeck_keyup_events(event,ai_settings,screen,ship,bullets)
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        aliens.empty()
        bullets.empty()
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        stats.game_active=True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key==pygame.K_RIGHT:
        ship.moving_right=True
    elif event.key==pygame.K_LEFT:
        ship.moving_left=True
    elif event.key==pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key==pygame.K_q:
        sys.exit()
def ckeck_keyup_events(event,ai_settings,screen,ship,bullets):
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT:
        ship.moving_left=False
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)#循环时重绘屏幕
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    sb.show_score()
    '''让绘制的屏幕可见'''
    pygame.display.flip()
def update_bullet(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)
        
    if len(aliens)==0:
        stats.level+=1
        sb.prep_level()
        bullets.empty()
        ai_settings.increase_speed()
        creat_fleet(ai_settings,screen,ship,aliens)

def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets)<ai_settings.bullet_allowed:
            new_bullet=Bullet(ai_settings,screen,ship)
            bullets.add(new_bullet)

def creat_fleet(ai_settings,screen,ship,aliens):
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    number_alien_x=get_number_aliens_x(ai_settings,alien_width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            creat_alien(ai_settings,screen,aliens,alien_number,row_number)

def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
    new_alien=Alien(ai_settings,screen)
    new_alien_width=new_alien.rect.width
    new_alien.x=new_alien_width+2*new_alien_width*alien_number
    new_alien.y=new_alien.rect.height+2*new_alien.rect.height*row_number
    new_alien.rect.x=new_alien.x
    new_alien.rect.y=new_alien.y
    aliens.add(new_alien)
    
def get_number_aliens_x(ai_settings,alien_width):
    avaliable_space_x=ai_settings.screen_width-2*alien_width
    number_aliens_x=int(avaliable_space_x/(2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    avaliable_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows=int(avaliable_space_y/(2*alien_height))
    return number_rows

def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
    chekc_fleet_edges(ai_settings,aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)

    check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets)

def chekc_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
    if stats.ship_left>0:
        stats.ship_left-=1

        sb.prep_ships()

        aliens.empty()
        bullets.empty()
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

    creat_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()
    sleep(0.5)

def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets):
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()
