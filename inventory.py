import pygame
from assets import key_img

image_path = "Assets/"

class ItemType:
    def __init__(self, name, icon, stack_size = 1):
        self.name = name
        self.icon_name = icon
        self.icon = pygame.image.load(image_path + icon)
        self.value = 0
        self.weight = 0
        self.stack_size = stack_size

class ItemSlot:
    def __init__(self, item_type=None, amount=0):
        self.item_type = item_type
        self.amount = amount

    def add_item(self, amount):
        self.amount += amount

    def remove_item(self, amount):
        self.amount -= amount
        if self.amount <= 0:
            self.item_type = None
            self.amount = 0

class Inventory:
    def __init__(self, num_slots, screen):
        self.slots = [ItemSlot() for _ in range(num_slots)]
        self.num_slots = num_slots
        self.screen = screen
        self.is_open = False
        
        # UI properties
        self.slot_size = 50
        self.padding = 10
        self.columns = 5
        rows = (num_slots + self.columns - 1) // self.columns
        self.inventory_width = (self.slot_size + self.padding) * self.columns + self.padding
        self.inventory_height = (self.slot_size + self.padding) * rows + self.padding
        self.inventory_x = (self.screen.get_width() - self.inventory_width) / 2
        self.inventory_y = (self.screen.get_height() - self.inventory_height) / 2
        
        # Placeholder UI elements
        self.background_color = (100, 100, 100, 180) # Semi-transparent gray
        self.slot_color = (50, 50, 50)
        self.font = pygame.font.Font(None, 24)

    def add_item(self, item_type):
        # Try to stack with existing items
        for slot in self.slots:
            if slot.item_type and slot.item_type.name == item_type.name and slot.amount < slot.item_type.stack_size:
                slot.add_item(1)
                return True

        # Find an empty slot
        for slot in self.slots:
            if not slot.item_type:
                slot.item_type = item_type
                slot.add_item(1)
                return True
        
        print("Inventory is full!")
        return False

    def draw(self):
        if not self.is_open:
            return

        # Create a semi-transparent surface for the background
        bg_surface = pygame.Surface((self.inventory_width, self.inventory_height), pygame.SRCALPHA)
        bg_surface.fill(self.background_color)
        self.screen.blit(bg_surface, (self.inventory_x, self.inventory_y))

        for i, slot in enumerate(self.slots):
            row = i // self.columns
            col = i % self.columns
            
            slot_x = self.inventory_x + self.padding + col * (self.slot_size + self.padding)
            slot_y = self.inventory_y + self.padding + row * (self.slot_size + self.padding)
            
            pygame.draw.rect(self.screen, self.slot_color, (slot_x, slot_y, self.slot_size, self.slot_size))

            if slot.item_type:
                icon_rect = slot.item_type.icon.get_rect(center=(slot_x + self.slot_size / 2, slot_y + self.slot_size / 2))
                self.screen.blit(slot.item_type.icon, icon_rect)
                
                if slot.amount > 1:
                    text = self.font.render(str(slot.amount), True, (255, 255, 255))
                    text_rect = text.get_rect(bottomright=(slot_x + self.slot_size - 2, slot_y + self.slot_size - 2))
                    self.screen.blit(text, text_rect)

class DroppedItem(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        self.image = self.item_type.icon
        self.rect = self.image.get_rect(topleft=(x, y))