function loadAssets() {
  const assets = {
      background: loadImage('resources/background.png'),
      sushi: loadImage('resources/sushi.png'),
      pipeTop: loadImage('resources/pipe_top.png'),
      pipeBottom: loadImage('resources/pipe_bottom.png'),
  };
  return assets;
}

function loadImage(src) {
  const img = new Image();
  img.src = src;
  return img;
}
