import pygame, random

pygame.init()

WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pesawat2an")

MERAH = (250, 50, 50)
PUTIH = (255, 255, 255)
HIJAU = (50, 250, 50)
HITAM = (10, 10, 10)

font = pygame.font.Font('Prototype.ttf', 24)

class E:
  def __init__(self):
    self.size = 70
    self.x = random.randint(50, WIDTH - self.size - 20)
    # self.x = WIDTH / 2
    # self.x = col
    self.y = -self.size
    self.char = "foto.png"
    # self.step = random.uniform(0.3, 1)
    self.step = 1
    self.__hp = 100 * 3

  def hpBar(self):
    pygame.draw.rect(screen, HIJAU, (WIDTH - 40 , 350, 20, -self.__hp), 0, 5)

  def hpDecrement(self):
    self.__hp -= 10

  def isDead(self):
    if self.__hp == 0:
      return True

  def reset(self):
    self.x = random.randint(50, WIDTH - self.size - 20)
    self.y = -self.size
    self.step = 1

  def show(self):
    charImg = pygame.image.load("i/" + self.char)
    charImg = pygame.transform.scale(charImg, (self.size, self.size))
    screen.blit(charImg, (self.x, self.y))

  def update(self):
    self.y += self.step

  def cekTepi(self):
    if self.y > HEIGHT:
      self.reset()


class Peluru:
  def __init__(self, p):
    self.size = 10
    self.x = p.x
    self.y = p.y
    self.x2 = p.x + p.size - self.size
    self.y2 = p.y
    self.langkah = 10
  
  def tampilkan(self):
    pygame.draw.rect(screen, MERAH, (self.x, self.y, self.size, self.size))
    pygame.draw.rect(screen, MERAH, (self.x2, self.y2, self.size, self.size))
  
  def gerak(self):
    self.y = self.y - self.langkah
    self.y2 = self.y2 - self.langkah

  def keatas(self):
    if self.y < 0 and self.y2 < 0:
      return True
  
  def hit(self, e):
    if self.x + self.size > e.x and self.x < e.x + e.size or \
      self.x2 + self.size > e.x and self.x2 < e.x + e.size:
      if self.y + self.size > e.y and self.y < e.y + e.size or \
        self.y2 + self.size > e.y and self.y2 < e.y + e.size:
          return True
  


class Pesawat:
  def __init__(self):
    self.size = 50
    self.x = WIDTH / 2
    self.y = HEIGHT - self.size - 10
    self.tombolKiri = False
    self.tombolKanan = False
    self.langkah = 5
  
  def tampilkan(self):
    gambar = pygame.image.load("i/pesawat.png")
    gambar = pygame.transform.scale(gambar, (self.size, self.size))
    screen.blit(gambar, (self.x, self.y))
    # pygame.draw.rect(screen, HIJAU, (self.x, self.y, self.size, self.size))

  def gerak(self):
    if self.tombolKanan:
      self.x = self.x + self.langkah
    if self.tombolKiri:
      self.x = self.x - self.langkah
  
  def cekTepi(self):
    if self.x < 0:
      self.x = 0
    if self.x > WIDTH - self.size:
      self.x = WIDTH - self.size


def winPropper():
  sprite_image = pygame.image.load("propper.gif").convert_alpha()
  sprite_image = pygame.transform.scale(sprite_image, (WIDTH, HEIGHT))
  screen.blit(sprite_image, (0,0))

def main():
  win = pygame.mixer.Sound("sound/win.mp3")
  pop = pygame.mixer.Sound("sound/pop.mp3")
  shot = pygame.mixer.Sound("sound/shot.wav")
  finish = False
  skor = 0
  run = True
  while run:
    for e in pygame.event.get():
      if e.type == pygame.QUIT:
        run = False
      
      # KEYDOWN
      if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
        run = False
      elif e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
        pesawat.tombolKanan = True
      elif e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
        pesawat.tombolKiri = True
      elif e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
        bullets.append(Peluru(pesawat))
        shot.play()
      elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
        finish = False
        pygame.display.update()

      # KEYUP
      if e.type == pygame.KEYUP:
        pesawat.tombolKanan = False
        pesawat.tombolKiri = False
      
    # BACKGROUND COLOR
    screen.fill(HITAM)

    # SKOR
    teks = font.render(str(skor), True, PUTIH)
    screen.blit(teks, (20, 20))

    # WIN?
    if en.isDead():
      winPropper()
      win.play()
      teks = font.render("YOU WIN!", True, MERAH)
      screen.blit(teks, (WIDTH/2, HEIGHT/2))
      pygame.display.update()
      finish = True

    # Ens
    en.update()
    en.show()
    en.cekTepi()
    en.hpBar()

    # PELULU
    for bullet in bullets:
      bullet.tampilkan()
      bullet.gerak()
      if bullet.keatas():
        bullets.remove(bullet)
      if bullet.hit(en):
        pop.play()
        bullets.remove(bullet)
        skor += 1
        en.hpDecrement()

    # PESAWAT
    pesawat.tampilkan()
    pesawat.gerak()
    pesawat.cekTepi()

    if not finish:
      pygame.display.update()


if __name__ == "__main__":
  pesawat = Pesawat()
  bullets = []
  en = E()
  
  main()