// Usage:
//   node render.mjs still <layout> <out.png> [t] [extra query]
//   node render.mjs video <layout> <out.mp4> [fps] [extra query]
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const [,, mode, layout, out, arg4, extra=''] = process.argv;
const SIZES = {launch:[1600,900], og:[1280,640], split:[1920,1080], phone:[1920,1080]};
const [W,H] = SIZES[layout];
const here = path.dirname(fileURLToPath(import.meta.url));
const url = `file://${here}/stage.html?layout=${layout}&theme=${process.env.THEME||'navy'}${extra ? '&'+extra : ''}`;

const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--no-sandbox','--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: mode==='still' ? 2 : 1 });
page.on('console', m => { if (m.type()==='error') console.error('page:', m.text()); });
await page.goto(url);
await page.evaluate(() => window.ready);
await page.waitForTimeout(300);

if (mode === 'still') {
  const t = arg4 !== undefined ? Number(arg4) : undefined;
  if (t !== undefined && !Number.isNaN(t)) await page.evaluate(t => window.seek(t), t);
  await page.waitForTimeout(100);
  await page.screenshot({ path: out, clip: { x:0, y:0, width:W, height:H } });
  console.log('wrote', out);
} else {
  const fps = Number(arg4 || 30);
  const duration = await page.evaluate(() => window.DURATION);
  const n = Math.round(duration * fps);
  const ff = spawn('ffmpeg', ['-y','-loglevel','error','-f','image2pipe','-framerate',String(fps),'-i','-',
    '-vf','format=yuv420p','-c:v','libx264','-preset','slow','-crf','19','-movflags','+faststart', out], { stdio: ['pipe','inherit','inherit'] });
  const t0 = Date.now();
  for (let i=0; i<n; i++) {
    await page.evaluate(t => window.seek(t), i/fps);
    const buf = await page.screenshot({ type: 'png', clip: { x:0, y:0, width:W, height:H } });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) process.stdout.write(`frame ${i}/${n} (${((Date.now()-t0)/1000).toFixed(0)}s)\n`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('wrote', out, `${n} frames @ ${fps}fps = ${duration}s`);
}
await browser.close();
