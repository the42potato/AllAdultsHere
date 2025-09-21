const optimal_gems = document.getElementById('optimal_gems');
const gem_calculator = document.getElementById('gem_calculator');

class Color {
    #name
    constructor(name) {
        this.#name = name;
    }
    getName() {
        return this.#name;
    }
}
class Slot {
    #shape
    constructor(shape) {
        this.#shape = shape;
    }
    getShape() {
        return this.#shape;
    }
}

const validSlots = {
    "circ": new Slot('circular'),
    "rect": new Slot('rectangular')
}
const validColors = {
    "red": new Color('red'),
    "blue": new Color('blue'),
    "yellow": new Color('yellow'),
    "purple": new Color('purple'),
    "green": new Color('green')
}

class Gem {
    #name
    #color
    #slot
    #value
    constructor(name, color, slot, value) {
        if (typeof name !== 'string') {
            throw new Error('Name must be a string');
        }
        if (!Object.values(validColors).includes(color)) {
            throw new Error('Color must be one of the valid Color objects');
        }
        if (slot instanceof Slot === false) {
            throw new Error('Color must be a Slot object');
        }
        if (!Object.values(validSlots).includes(slot)) {
            throw new Error('Slot must be one of the valid Slot objects');
        }
        if (typeof value !== 'number') {
            throw new Error('value must be a number');
        }
        this.#name = name;
        this.#color = color;
        this.#slot = slot;
        this.#value = Math.floor(value / 1000) * 1000;
    }
    getName() {
        return this.#name;
    }
    getColor() {
        return this.#color;
    }
    getSlot() {
        return this.#slot;
    }
    getValue() {
        return this.#value;
    }
}

class Treasure {
    #name
    #slots
    #value
    constructor(name, slots, value) {
        if (typeof name !== 'string') {
            throw new Error('Name must be a string');
        }
        if (!Array.isArray(slots)) {
            throw new Error('gems must be an array');
        }
        if (!slots.every(slot => slot instanceof Slot)) {
            throw new Error('All elements in gems must be instances of Slot');
        }
        if (typeof value !== 'number') {
            throw new Error('value must be a number');
        }
        this.#name = name;
        this.#slots = slots;
        this.#value = value;
    }
    getName() {
        return this.#name;
    }
    getSlots() {
        return this.#slots;
    }
    getSlotCount() {
        return this.#slots.length;
    }
    getValue() {
        return this.#value;
    }
}

const validGems = {
    "ruby": new Gem('Red Ruby', validColors.red, validSlots.circ, 3000),
    "sapphire": new Gem('Blue Sapphire', validColors.blue, validSlots.circ, 4000),
    "diamond": new Gem('Yellow Diamond', validColors.yellow, validSlots.circ, 7000),
    "emerald": new Gem('Green Emerald', validColors.green, validSlots.circ, 5000),
    "alexandrite": new Gem('Purple Alexandrite', validColors.purple, validSlots.circ, 6000),
    "beryl": new Gem('Red Beryl', validColors.red, validSlots.circ, 9000)
}
const validTreasures = {
    "crown": new Treasure('Elegant Crown', [validSlots.rect, validSlots.circ, validSlots.rect, validSlots.circ, validSlots.rect], 19000),
    "necklace": new Treasure('Ornate Necklace', [validSlots.rect, validSlots.circ, validSlots.circ, validSlots.rect], 11000),
    "chalice": new Treasure("Chalice of Atonement", [validSlots.rect, validSlots.rect, validSlots.rect], 7000),
    "mask": new Treasure("Elegant Mask", [validSlots.circ, validSlots.circ, validSlots.circ], 5000),
    "lamp": new Treasure("Butterfly Lamp", [validSlots.circ, validSlots.circ, validSlots.circ], 6000),
    "lynx": new Treasure("Golden Lynx", [validSlots.circ, validSlots.rect, validSlots.circ], 15000),
    "flagon": new Treasure("Flagon", [validSlots.circ, validSlots.circ], 4000),
    "elegant_bangle": new Treasure("Elegant Bangle", [validSlots.circ, validSlots.circ], 5000),
    "splendid_bangle": new Treasure("Splendid Bangle", [validSlots.rect, validSlots.rect], 4000),
    "clock": new Treasure("Extravagent Clock", [validSlots.circ, validSlots.rect], 9000),
}

Object.values(validTreasures).forEach(treasure => {
    let bestValue = treasure.value;
    let bestCombo = [];
});