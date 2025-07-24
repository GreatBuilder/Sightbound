import pygame
from item_type import ItemType
from assets import inv_slot_img, inv_select_img, key_pickup_sound, key_drop_sound, key_item
from settings import display_width, display_height

class Inventory:
    def __init__(self):
        self.items = []
        self.inv_slot_img = inv_slot_img
        self.inv_select_img = inv_select_img
        self.slot_size = self.inv_slot_img.get_width()
        self.padding = 5
        self.is_open = True # Let's keep it open for now to see it
        self.selected_slot = 0

    def add_item(self, item):
        if len(self.items) < 4:
            self.items.append(item)
            print(f"Added {item.name} to inventory.")
            if item == key_item:
                key_pickup_sound.play()
        else:
            print("Inventory is full!")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def drop_item(self):
        if 0 <= self.selected_slot < len(self.items):
            item_to_drop = self.items.pop(self.selected_slot)
            return item_to_drop
        return None

    def get_selected_item(self):
        if 0 <= self.selected_slot < len(self.items):
            return self.items[self.selected_slot]
        return None

    def draw(self, surface):
        if not self.is_open:
            return

        # Draw slots and items first
        for i in range(4):
            slot_x = (display_width // 2) - (2 * (self.slot_size + self.padding)) + i * (self.slot_size + self.padding)
            slot_y = display_height - self.slot_size - self.padding
            surface.blit(self.inv_slot_img, (slot_x, slot_y))
            if i < len(self.items):
                item = self.items[i]
                item_img = item.inv_img
                img_rect = item_img.get_rect(center=(slot_x + self.slot_size // 2, slot_y + self.slot_size // 2))
                surface.blit(item_img, img_rect)

        # Then draw the selection image on top
        selected_slot_x = (display_width // 2) - (2 * (self.slot_size + self.padding)) + self.selected_slot * (self.slot_size + self.padding)
        selected_slot_y = display_height - self.slot_size - self.padding
        if self.selected_slot == 0:
            surface.blit(self.inv_select_img, (selected_slot_x, selected_slot_y))
        elif self.selected_slot == 1:
            surface.blit(self.inv_select_img, (selected_slot_x, selected_slot_y)) 
        elif self.selected_slot == 2:
            surface.blit(self.inv_select_img, (selected_slot_x, selected_slot_y))
        elif self.selected_slot == 3:
            surface.blit(self.inv_select_img, (selected_slot_x, selected_slot_y))