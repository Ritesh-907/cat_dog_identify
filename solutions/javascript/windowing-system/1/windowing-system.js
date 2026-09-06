// @ts-check

// ============================================
// Task 1: Size
// ============================================

export function Size(width = 80, height = 60) {
  this.width = width;
  this.height = height;
}

Size.prototype.resize = function (newWidth, newHeight) {
  this.width = newWidth;
  this.height = newHeight;
};


// ============================================
// Task 2: Position
// ============================================

export function Position(x = 0, y = 0) {
  this.x = x;
  this.y = y;
}

Position.prototype.move = function (newX, newY) {
  this.x = newX;
  this.y = newY;
};


// ============================================
// Task 3: ProgramWindow
// ============================================

export class ProgramWindow {
  constructor() {
    this.screenSize = new Size(800, 600);
    this.size = new Size();
    this.position = new Position();
  }


  // ==========================================
  // Task 4: Resize the window
  // ==========================================

  resize(newSize) {
    this.size.width = Math.max(
      1,
      Math.min(
        newSize.width,
        this.screenSize.width - this.position.x
      )
    );

    this.size.height = Math.max(
      1,
      Math.min(
        newSize.height,
        this.screenSize.height - this.position.y
      )
    );
  }


  // ==========================================
  // Task 5: Move the window
  // ==========================================

  move(newPosition) {
    this.position.x = Math.max(
      0,
      Math.min(
        newPosition.x,
        this.screenSize.width - this.size.width
      )
    );

    this.position.y = Math.max(
      0,
      Math.min(
        newPosition.y,
        this.screenSize.height - this.size.height
      )
    );
  }
}


// ============================================
// Task 6: Change the window
// ============================================

export function changeWindow(programWindow) {
  programWindow.resize(new Size(400, 300));

  programWindow.move(new Position(100, 150));

  return programWindow;
}