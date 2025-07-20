import pygame
from item_type import ItemType

class Inventory:
    def __init__(self, inv_slot_img):
        self.items = []
        self.inv_slot_img = inv_slot_img
        self.slot_size = self.inv_slot_img.get_width()
        self.padding = 5
        self.is_open = True # Let's keep it open for now to see it

    def add_item(self, item):
        if len(self.items) < 4:
            self.items.append(item)
            print(f"Added {item.name} to inventory.")
        else:
            print("Inventory is full!")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def draw(self, surface):
        if not self.is_open:
            return

        for i in range(4):
            slot_x = 3 + i * (self.slot_size + self.padding)
            slot_y = 3
            surface.blit(self.inv_slot_img, (slot_x, slot_y))
            if i < len(self.items):
                item = self.items[i]
                item_img = item.inv_img
                img_rect = item_img.get_rect(center=(slot_x + self.slot_size // 2, slot_y + self.slot_size // 2))
                surface.blit(item_img, img_rect)