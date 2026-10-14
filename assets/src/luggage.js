// Clay-style luggage pile for three.js. Usage:
//   const L = await createLuggage(container, {width, height}); L.seek(t); L.render();
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

const clay = (hex, rough = 0.92) => new THREE.MeshStandardMaterial({ color: hex, roughness: rough, metalness: 0 });
const easeOut = x => 1 - Math.pow(1 - x, 3);
const easeOutQuint = x => 1 - Math.pow(1 - x, 5);

function suitcase({ w, h, d, color, trim = 0x1C2430, ribs = 3, tag = null, wheels = true }) {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 8, Math.min(w, h, d) * 0.22), clay(color));
  body.castShadow = body.receiveShadow = true; g.add(body);
  // horizontal ribs on the front face (lying-flat case: "front" is +z)
  const ribMat = clay(color, 0.7); ribMat.color.offsetHSL(0, 0, -0.02);
  for (let i = 0; i < ribs; i++) {
    const y = -h / 2 + (h * (i + 1)) / (ribs + 1);
    const rib = new THREE.Mesh(new RoundedBoxGeometry(w * 0.86, h * 0.06, 0.035, 3, 0.015), ribMat);
    rib.position.set(0, y, d / 2 + 0.012); rib.castShadow = true; g.add(rib);
    const rib2 = rib.clone(); rib2.position.z = -d / 2 - 0.012; g.add(rib2);
  }
  // top carry handle (on +x end, since the case lies flat and the handle points sideways)
  const handle = new THREE.Mesh(new RoundedBoxGeometry(0.16, 0.14, d * 0.42, 4, 0.06), clay(trim, 0.85));
  handle.position.set(w / 2 + 0.06, 0, 0); handle.castShadow = true; g.add(handle);
  // wheels on the -x end
  if (wheels) {
    const wm = clay(trim, 0.9);
    for (const sz of [-1, 1]) {
      const wh = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.09, 24), wm);
      wh.rotation.z = Math.PI / 2; wh.position.set(-w / 2 - 0.02, -h / 2 + 0.16, sz * (d / 2 - 0.16)); wh.castShadow = true; g.add(wh);
    }
  }
  if (tag) {
    const t = new THREE.Mesh(new RoundedBoxGeometry(0.34, 0.5, 0.05, 3, 0.05), clay(tag, 0.6));
    t.position.set(w / 2 - 0.1, h / 2 - 0.02, d / 2 + 0.22); t.rotation.set(0.25, 0, -0.35); t.castShadow = true; g.add(t);
    const strap = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.02, 10, 24), clay(0xE8E8EC, 0.5));
    strap.position.set(w / 2 - 0.03, h / 2 + 0.08, d / 2 + 0.1); strap.rotation.y = 0.6; g.add(strap);
  }
  return g;
}

export async function createLuggage(container, { width, height, dpr = 1, bg = null }) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(dpr); renderer.setSize(width, height);
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  if (bg) scene.background = new THREE.Color(bg);
  const camera = new THREE.PerspectiveCamera(26, width / height, 0.1, 100);
  camera.position.set(6.2, 5.0, 8.2); camera.lookAt(0, 1.15, 0);

  scene.add(new THREE.HemisphereLight(0xFFFFFF, 0x2A4A7F, 1.1));
  const key = new THREE.DirectionalLight(0xFFF4E6, 1.7); key.position.set(5, 9, 6); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); key.shadow.radius = 8; key.shadow.bias = -0.0005;
  key.shadow.camera.left = -6; key.shadow.camera.right = 6; key.shadow.camera.top = 6; key.shadow.camera.bottom = -6;
  scene.add(key);
  const fill = new THREE.DirectionalLight(0xFFFFFF, 0.7); fill.position.set(-6, 3, 2); scene.add(fill);
  const rim = new THREE.DirectionalLight(0xFFFFFF, 0.3); rim.position.set(-2, 6, -7); scene.add(rim);

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: 0.18 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);

  // the pile: three cases lying flat, largest at the bottom
  const specs = [
    { w: 3.0, h: 0.95, d: 2.1, color: 0x2F5A99, ribs: 3, y: 0.475, rot: 0.10, delay: 0.00 },
    { w: 2.5, h: 0.85, d: 1.8, color: 0xE7DECF, ribs: 2, y: 0.95 + 0.425, rot: -0.16, delay: 0.22 },
    { w: 1.75, h: 0.62, d: 1.3, color: 0xC7AB84, ribs: 2, y: 1.8 + 0.31, rot: 0.22, delay: 0.40, tag: 0xC0392B, trim: 0x2A2A32 },
  ];
  const cases = specs.map(sp => { const c = suitcase(sp); c.position.set(0, sp.y, 0); c.rotation.y = sp.rot; scene.add(c); return { obj: c, sp }; });
  const pile = new THREE.Group(); // (kept simple: cases are direct children of the scene)

  function seek(t, { intro = 1.3 } = {}) {
    // intro: cases settle into place from slightly above, fading in; afterwards a slow 2-degree sway
    for (const { obj, sp } of cases) {
      const p = Math.max(0, Math.min(1, (t - sp.delay) / (intro - 0.45)));
      const e = easeOutQuint(p);
      obj.position.y = sp.y + (1 - e) * 2.2;
      obj.visible = p > 0;
      obj.rotation.y = sp.rot + (1 - e) * 0.25;
    }
    scene.rotation.y = 0;
  }
  function render() { renderer.render(scene, camera); }
  seek(10); render();
  return { seek, render, renderer, scene, camera };
}
