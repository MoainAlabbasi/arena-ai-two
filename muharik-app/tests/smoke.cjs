// Requires Playwright. Start a static server first; BASE_URL can override localhost.
const { chromium } = require('playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:8083/';
(async () => {
  const browser = await chromium.launch({headless:true, args:['--no-sandbox','--enable-webgl','--use-angle=swiftshader']});
  try {
    for (const viewport of [{width:1400,height:900},{width:390,height:844}]) {
      const context = await browser.newContext({viewport}); const page=await context.newPage(); const errors=[];
      page.on('pageerror',e=>errors.push(e.message));
      await page.goto(base,{waitUntil:'domcontentloaded'}); await page.locator('.hero-copy h1').waitFor();
      if (await page.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth)) throw Error('Horizontal overflow');
      await page.goto(base+'#search'); await page.locator('#searchInput').fill('٤٧٨٧٣٦');
      if (!(await page.locator('.result-card').first().innerText()).includes('478736')) throw Error('Part search failed');
      await page.locator('[data-page="54"]').first().click(); await page.locator('#pageImg').waitFor();
      await page.locator('#savePage').click(); await page.goto(base+'#saved');
      if ((await page.locator('.page-tile').count())!==1) throw Error('Favorites failed');
      await page.goto(base+'#manual'); if ((await page.locator('.page-tile').count())!==56) throw Error('Page count failed');
      await page.goto(base+'#lab'); await page.frameLocator('.lab-frame').locator('canvas').waitFor();
      if (errors.length) throw Error(errors.join('; '));
      console.log('OK viewport',viewport.width,viewport.height); await context.close();
    }
  } finally { await browser.close() }
})().catch(e=>{console.error(e);process.exit(1)});
