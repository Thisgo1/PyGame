from os import walk
import pygame

def import_folder(path):
  surface_list = []
  
  for _, _, img_files in walk(path):
    for image in img_files:
      full_path = path + "/" + image
      image_surface = pygame.image.load(full_path).convert_alpha()#convertendo para algo que funciona muito melhor no pygame
      surface_list.append(image_surface)
  
  return surface_list
