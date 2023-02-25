// sample_068
//
// GLSL だけでレンダリングする
// https://wgld.org/d/glsl/g001.html

// を、参照。一部改変

// global
let gl;
const uniLocation = new Array();

let cnvs, cnvsWidth, cnvsHeight;
let mouseX = 0.5;
let mouseY = 0.5;

// render ループ関係
let time = 0.0;
let prevTimestamp = 0;
const FPS = 120;
const frameTime = 1 / FPS;

// シェーダーコード関係
let prevFragmentCode = '';

const vs = './shaders/vertex/vertexMain.js';
const fs = './shaders/fragment/fragmentMain.js';

const vertexPrimitive = await fetchShader(vs);
const fragmentPrimitive = await fetchShader(fs);

async function fetchShader(path) {
  const res = await fetch(path);
  const shaderText = await res.text();
  return shaderText;
}

const setupDOM = () => {
  const wrapDiv = document.createElement('div');
  wrapDiv.id = 'wrap';
  const canvas = document.createElement('canvas');
  canvas.id = 'myCanvas';
  const textArea = document.createElement('textarea');
  textArea.id = 'textArea';
  textArea.value = fragmentPrimitive;
  textArea.style.width = '100%';
  textArea.style.height = '100%';
  document.body.appendChild(wrapDiv);
  wrapDiv.appendChild(canvas);
  wrapDiv.appendChild(textArea);

  textArea.addEventListener('input', (event) => {
    const textareaValue = event.target.value;
    const fragCode = textareaValue.replace(/\r?\n/g, '');
    if (prevFragmentCode != fragCode) {
      setupGL(vertexPrimitive, textareaValue);
      prevFragmentCode = fragCode;
    }
  });
};

setupDOM();
window.addEventListener('load', setupGL(vertexPrimitive, fragmentPrimitive));

function setupGL(vertexSource, fragmentSource) {
  // todo: js で生成しているのであれば、編集より取得でもいいかも
  // 画面サイズよりcanvas サイズを設定
  cnvsWidth = document.querySelector('#wrap').clientWidth;
  cnvsHeight = cnvsWidth * 0.64; // いい感じのサイズ調整
  // canvas エレメントを取得
  cnvs = document.querySelector('#myCanvas');
  cnvs.width = cnvsWidth;
  cnvs.height = cnvsHeight;

  // イベントリスナー登録
  // todo: touch イベントへ
  cnvs.addEventListener('mousemove', mouseMove, true);

  gl = cnvs.getContext('webgl2');
  // プログラムオブジェクトの生成とリンク
  const prg = create_program(
    // 頂点シェーダとフラグメントシェーダの生成
    create_shader('vs', vertexSource),
    create_shader('fs', fragmentSource)
  );
  uniLocation[0] = gl.getUniformLocation(prg, 'time');
  uniLocation[1] = gl.getUniformLocation(prg, 'mouse');
  uniLocation[2] = gl.getUniformLocation(prg, 'resolution');

  // 頂点データ回りの初期化
  const position = [
    -1.0, 1.0, 0.0, 1.0, 1.0, 0.0, -1.0, -1.0, 0.0, 1.0, -1.0, 0.0,
  ];
  const index = [0, 2, 1, 1, 2, 3];

  const vPosition = create_vbo(position);
  const vIndex = create_ibo(index);
  const vAttLocation = gl.getAttribLocation(prg, 'position');

  gl.bindBuffer(gl.ARRAY_BUFFER, vPosition);
  gl.enableVertexAttribArray(vAttLocation);
  gl.vertexAttribPointer(vAttLocation, 3, gl.FLOAT, false, 0, 0);
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, vIndex);

  // その他の初期化
  gl.clearColor(0.0, 0.0, 0.0, 1.0);
  mouseX = 0.5;
  mouseY = 0.5;

  renderLoop(); // レンダリング関数呼出
}

function renderLoop(timestamp) {
  const elapsed = (timestamp - prevTimestamp) / 1000;
  if (elapsed <= frameTime) {
    requestAnimationFrame(renderLoop);
    return;
  }
  prevTimestamp = timestamp;
  time += frameTime;
  glRender(time);
  requestAnimationFrame(renderLoop); // 再帰
}

function glRender(time) {
  gl.clear(gl.COLOR_BUFFER_BIT); // カラーバッファをクリア
  // uniform 関連
  gl.uniform1f(uniLocation[0], time);
  gl.uniform2fv(uniLocation[1], [mouseX, mouseY]);
  gl.uniform2fv(uniLocation[2], [cnvsWidth, cnvsHeight]);
  gl.drawElements(gl.TRIANGLES, 6, gl.UNSIGNED_SHORT, 0); // 描画
  gl.flush();
}

// mouse
function mouseMove(e) {
  mouseX = e.offsetX / cnvsWidth;
  mouseY = e.offsetY / cnvsHeight;
}

/* シェーダを生成・コンパイルする関数 */
function create_shader(type, text) {
  let shader;
  // scriptタグのtype属性をチェック
  switch (type) {
    case 'vs': // 頂点シェーダの場合
      shader = gl.createShader(gl.VERTEX_SHADER);
      break;
    case 'fs': // フラグメントシェーダの場合
      shader = gl.createShader(gl.FRAGMENT_SHADER);
      break;
    default:
      return;
  }

  gl.shaderSource(shader, text); // 生成されたシェーダにソースを割り当てる
  gl.compileShader(shader); // シェーダをコンパイルする
  // シェーダが正しくコンパイルされたかチェック
  if (gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    return shader; // 成功していたらシェーダを返して終了
  } else {
    // 失敗していたらエラーログをアラートしコンソールに出力
    // alert(gl.getShaderInfoLog(shader));
    console.log(gl.getShaderInfoLog(shader));
  }
}

// プログラムオブジェクトを生成しシェーダをリンクする関数
function create_program(vs, fs) {
  const program = gl.createProgram(); // プログラムオブジェクトの生成

  // プログラムオブジェクトにシェーダを割り当てる
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program); // シェーダをリンク

  // シェーダのリンクが正しく行なわれたかチェック
  if (gl.getProgramParameter(program, gl.LINK_STATUS)) {
    gl.useProgram(program); // 成功していたらプログラムオブジェクトを有効にする
    return program; // プログラムオブジェクトを返して終了
  } else {
    return null; // 失敗していたら NULL を返す
  }
}

// VBOを生成する関数
function create_vbo(data) {
  const vbo = gl.createBuffer(); // bufferObject の生成

  gl.bindBuffer(gl.ARRAY_BUFFER, vbo); // buffer をバインドする
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW); // buffer にデータをセット
  gl.bindBuffer(gl.ARRAY_BUFFER, null); // buffer のバインドを無効化

  return vbo; // 生成した VBO を返して終了
}

// IBOを生成する関数
function create_ibo(data) {
  const ibo = gl.createBuffer(); // bufferObjectの生成

  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo); // buffer をバインド
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Int16Array(data), gl.STATIC_DRAW); // buffer にデータをセット
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, null); // buffer のバインドを無効化

  return ibo; // 生成したIBOを返し終了
}
