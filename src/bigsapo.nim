import raylib
import std/[random, strformat]

const
  scrn_width = 800
  scrn_height = 600



type
  Frog = object
    pos: Vector2
    color = Green
  Fly = ref object
    pos: Vector2
    color = Gray
    speed = 4
    


var 
  sapo: Image
  tongue = 0
  tongue_pos = Vector2(x:0, y:0)
  points: int32 = 0
  frog = Frog(pos: Vector2(x: scrn_width div 2, y: (scrn_height div 8)*4))
  flyarray = [
    Fly(pos: Vector2(x: rand(scrn_width).toFloat, y: rand(scrn_height).toFloat)),
    Fly(pos: Vector2(x: rand(scrn_width).toFloat, y: rand(scrn_height).toFloat)),
    Fly(pos: Vector2(x: rand(scrn_width).toFloat, y: rand(scrn_height).toFloat)),
    Fly(pos: Vector2(x: rand(scrn_width).toFloat, y: rand(scrn_height).toFloat)),
    Fly(pos: Vector2(x: rand(scrn_width).toFloat, y: rand(scrn_height).toFloat)),
  ]

proc draw =
    beginDrawing()
    clearBackground(RayWhite)
    drawTexture(sapo.loadTextureFromImage, Vector2(x: frog.pos.x-150.0, y: frog.pos.y-150.0), 0, 2, White)
    drawRectangleGradientV(0, (scrn_height div 8)*5, scrn_width, scrn_height div 2, SkyBlue, Blue)
    
    drawCircle(frog.pos, 5, frog.color)
    
    for f in flyarray:
      drawCircle(f.pos, 10, f.color)
    
    if tongue > 0:
      drawLine(frog.pos, tongue_pos, 6, Pink)
      tongue -= 1
      

    drawText(&"flys eaten: {points}", 20, 70, 20, LightGray)
    endDrawing()

proc update =
  var mpos = getMousePosition()
  for f in flyarray:
    f.pos.x += f.speed
    if f.pos.x - 50 > scrn_width:
      f.pos.x = -50
      f.pos.y = rand(scrn_height).toFloat
    
    if checkCollisionPointCircle(mpos, f.pos, 10) and isMouseButtonPressed(MouseButton.Left):
      tongue_pos = mpos
      tongue = 50
      f.pos.x = -50
      f.pos.y = rand(scrn_height).toFloat
      points += 1

proc init =
  initWindow(scrn_width, scrn_height, "big sapo")
  sapo = loadImage("src/arqueiro.png")
  imageAlphaClear(sapo, Color(r: 46, g: 46, b: 46, a: 255), 50)
  imageResize(sapo, 150, 150)



proc main =
  setTargetFPS(30)
  while not windowShouldClose(): # Detect window close button or ESC key
    draw()
    update()

  closeWindow()

init()
main()

