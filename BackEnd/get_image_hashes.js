const puppeteer = require('puppeteer');
const axios = require('axios');
const crypto = require('crypto');

async function fetchHTML(url) {
  const response = await axios.get(url);
  return response.data;
}

async function calculateMD5Hashes(url) {
  const html = await fetchHTML(url);

  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent(html);

  // Extract image URLs using JavaScript execution in the headless browser
  const imageSrcs = await page.evaluate(() => {
    const images = document.querySelectorAll('img');
    return Array.from(images)
    .map(img => img.src)
    .filter(src => src.startsWith('http://') || src.startsWith('https://'));
})

  // Calculate MD5 hashes for each image
  const md5Hashes = await Promise.all(
    imageSrcs.map(async imageUrl => {
      const response = await axios.get(imageUrl, { responseType: 'arraybuffer' });
      const imageData = Buffer.from(response.data, 'binary');
      const md5Hash = crypto.createHash('md5').update(imageData).digest('hex');
      return md5Hash;
    })
  );

  await browser.close();

  return md5Hashes;
}

// Example usage
const url = 'https://uzum.uz';
calculateMD5Hashes(url)
  .then(md5Hashes => {
    console.log('MD5 Hashes:');
    md5Hashes.forEach((md5Hash, index) => {
      console.log(`Image ${index + 1}: ${md5Hash}`);
    });
  })
  .catch(error => {
    console.error('Error calculating MD5 hashes:', error);
  });
