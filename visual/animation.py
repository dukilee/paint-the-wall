# from main import engine
# from resources import constants
#
# class Animation:
#     def interpolate(self, s, f, finalFrame, actualFrame, startingFrame = 0):
#         #interpolates from s to f in (finalFrame - startingFrame) intervals and return actualFrame value
#         return (f - s) * (actualFrame - startingFrame) / (finalFrame - startingFrame) + s
#
#
#     def animate(self, screen):
#         pass
#
# class MainMenuAnimation(Animation):
#     def __init__(self):
#         self.r1 = menu.Rectangle(650, 0, constants.HERO_SIZE[0], constants.HERO_SIZE[1], constants.RED)
#         self.r2 = menu.Rectangle(650, 0, constants.SCALE[0], constants.SCALE[1], constants.LIGHT_GREEN)
#         self.r3 = menu.Rectangle(150, 0, constants.SCALE[0], 0, constants.LIGHT_GREEN)
#
#     def update(self, screen, actualFrame):
#         actualFrame %= 2100
#         if actualFrame<500:
#             self.r1.x = 650
#             self.r1.y = self.interpolate(0, 800, 500, actualFrame)
#             self.r2.height = self.interpolate(0, 800, 500, actualFrame)
#         elif actualFrame<1000:
#             actualFrame -= 500
#             self.r1.x = 150
#             self.r1.y = self.interpolate(0, 800, 500, actualFrame)
#             self.r3.height = self.interpolate(0, 800, 500, actualFrame)
#         elif actualFrame<1500:
#             actualFrame -= 1000
#             self.r1.x = 650
#             self.r1.y = self.interpolate(800, 0, 500, actualFrame)
#             self.r2.height = self.interpolate(800, 0, 500, actualFrame)
#         elif actualFrame<2000:
#             actualFrame -= 1500
#             self.r1.x = 150
#             self.r1.y = self.interpolate(800, 0, 500, actualFrame)
#             self.r3.height = self.interpolate(800, 0, 500, actualFrame)
#
#         if actualFrame<2000:
#             self.r1.blit(screen)
#             self.r2.blit(screen)
#             self.r3.blit(screen)