PImage img;

int postItWidth = 15;
int postItHeight = 11;
// still need to manualaly input these
int canvasWidth = 1155;
int canvasHeight = 792;

void setup() {
  size(1155, 792);
  // Images must be in the "data" directory to load correctly
  img = loadImage("city.jpeg");
}

void draw() {
  image(img, 0, 0);
  img.resize(canvasWidth, 0);
  ArrayList arr = new ArrayList();
  
  for (int i = 0; i < canvasWidth; i += postItWidth) {
    for (int j = 0; j < canvasHeight; j += postItHeight) {
      PImage subImg = img.get(i, j, postItWidth, postItHeight);
      color c = extractColorFromSubImg(subImg);
      arr.add(c);
    }
  }
  
  int cIndex = 0;
  for (int i = 0; i < canvasWidth; i += postItWidth) {
    for (int j = 0; j < canvasHeight; j += postItHeight) {
      int c = arr.get(cIndex);
      fill(c);
      noStroke();
      rect(i, j, postItWidth, postItHeight);
    }
  }
}

color extractColorFromSubImg(PImage img) {
  int r = 0;
  int g = 0;
  int b = 0;
  for (int i = 0; i < img.pixels.length; i++) {
    color c = img.pixels[i];
    r += c >> 020 & 0xFF;
    g += c >> 010 & 0xFF;
    b += c        & 0xFF;
  }
  r /= img.pixels.length;
  g /= img.pixels.length;
  b /= img.pixels.length;
 
  return color(r, g, b);
}