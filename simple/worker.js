import createModule from 'https://unpkg.com/@jspawn/imagemagick-wasm/magick.mjs';


onmessage = async function(e) {
  postMessage(null);
  postMessage('処理中… (けっこう時間かかるかも)');

  console.log('Worker: Message received from main script');
  console.log(e);

  const inputFile = e.data[0];

  const magick = await createModule({
    locateFile: () => 'https://unpkg.com/@jspawn/imagemagick-wasm/magick.wasm',
  });

  magick.FS.createLazyFile('/', 'palette.png', 'palette.png', true, false);


  // postMessage(pngBlob);

  magick.FS.mkdir('/working');
  magick.FS.mount(
    magick.WORKERFS,
    {
      blobs: [
        { name: 'sample.png', data: inputFile },
      ],
    },
    '/working'
  );

  magick.callMain([
    'working/sample.png',
    '-resize',
    '320x240',
    '+sigmoidal-contrast',
    '8,50%',
    '-modulate',
    '100,200,100',
    '-ordered-dither',
    '4x4,8,8,8',
    '+dither',
    '-remap',
    'palette.png',
    '-sample',
    '200%',
    'out.png'
  ]);

  const webpBuf = magick.FS.readFile('out.png');
  const webpBlob = new Blob([webpBuf], { type: 'image/png' });

  postMessage(webpBlob);
  postMessage('')
};
