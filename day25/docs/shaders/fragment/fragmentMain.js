#version 300 es
precision highp float;

out vec4 fragColor;

uniform float time;
uniform vec2 mouse;
uniform vec2 resolution;

void main() {
  vec2 p = (gl_FragCoord.xy * 2.0 - resolution) / min(resolution.x, resolution.y);
  vec3 outColor = vec3(p, abs(tan(time)));

  fragColor = vec4(outColor, 1.0);
}
