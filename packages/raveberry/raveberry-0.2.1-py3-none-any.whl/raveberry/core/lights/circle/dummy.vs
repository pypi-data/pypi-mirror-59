#version 300 es
precision mediump float;

in vec3 vertex;

void main(void) {
	gl_Position = vec4(vertex.xyz, 1);
}
