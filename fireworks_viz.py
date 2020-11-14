from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


import time
import numpy as np
from vispy import gloo, app
import vispy
from vispy.app import use_app
use_app('PyQt5')


class Canvas(app.Canvas):

    def __init__(self,ens_n,spks_,pos,U):
        app.Canvas.__init__(self,keys='interactive', size=(800, 600))

        self.U=U
        self.spks_=spks_
        #self.pos=(pos[:]*2)-1
        self.pos=pos
        self.ens_n=ens_n

        print('pos shp: ',self.pos)

        print(self.spks_)


        radius = 32
        self.im1 = np.random.normal(
            0.8, 0.3, (radius * 2 + 1, radius * 2 + 1)).astype(np.float32)

        # Mask it with a disk
        L = np.linspace(-radius, radius, 2 * radius + 1)
        (X, Y) = np.meshgrid(L, L)
        self.im1 *= np.array((X ** 2 + Y ** 2) <= radius * radius, dtype='float32')

        self.N = self.U.shape[0]
        print('N: ',self.N)

        # Create vertex data container
        self.data = np.zeros(self.N, [('a_position', np.float32, 3),
                            ('a_color', np.float32, 4),
                            ('a_lifetime',np.float32)])


        VERT_SHADER = """
        uniform float u_time;
        attribute vec3 a_position;
        attribute vec4 a_color;
        attribute float a_lifetime;
        varying float color_;
        varying float v_lifetime;

        void main () {
            gl_Position.xyz = a_position;

            color_=a_color.a;

            //gl_PointSize = 5.0;

            v_lifetime = 1.0 - (u_time / a_lifetime);
            v_lifetime = clamp(v_lifetime, 0.0, 1.0);

            gl_PointSize = (v_lifetime * v_lifetime) * 20.0;

        }
        """

        from vispy.app import use_app
        use_app('PyQt5')
        # Deliberately add precision qualifiers to test automatic GLSL code conversion
        FRAG_SHADER = """
        #version 120
        uniform vec4 u_color;
        precision highp float;
        uniform sampler2D texture1;
        varying float color_;
        uniform highp sampler2D s_texture;
        void main()
        {
            highp vec4 texColor;
            texColor = texture2D(s_texture, gl_PointCoord);
            gl_FragColor = vec4(u_color) * texColor;
            gl_FragColor.a = color_;

        }
        """
        global i
        i=0
        # Create program
        self._program = gloo.Program(VERT_SHADER, FRAG_SHADER)
        self._program.bind(gloo.VertexBuffer(self.data))
        self._program['s_texture'] = gloo.Texture2D(self.im1)
        self.transp=self.spks_.T
        print('transp',self.transp.shape)

        self.i=0

        self.ens_n=ens_n
        self.ensemble=self.U[:,ens_n]

        # Create first explosion
        self._new_explosion()

        # Enable blending
        gloo.set_state(blend=True, clear_color='black',
                       blend_func=('src_alpha', 'one'))

        gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])

        self._timer = app.Timer('auto', connect=self.update, start=True)


    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):

        # Clear
        gloo.clear()

        # Draw
        self._program['u_time'] = time.time() - self._starttime

        # New explosion?
        if time.time() - self._starttime >1:
            self._new_explosion()

        self._program.draw('points')

    def _new_explosion(self):
        global i
        print(i)
        i+=1
        #self.i+=1

        #self._program['u_centerPosition'] = centerpos

        # New color, scale alpha with N
        a_transp=self.transp[i,:]
        print(sum(a_transp))

        color=np.ones((self.N,4))


        color[:,3]=a_transp*self.ensemble
        print('debug, ',color[:,3].sum())

        alpha = 1000.0 / self.N ** 0.08
        color_un = np.random.uniform(0.1, 0.9, (3,))

        self._program['u_color'] = tuple(color_un) + (alpha,)
        #self._program['color'] = color.astype('float32')

        # bind the VBO to the GL context
        #self._program.bind(self.data_vbo)
        self.data['a_color'] = color


        self.data['a_lifetime'] = np.random.normal(2.0, 0.5, (self.N,))

        self.data['a_position'] = self.pos

        print('texture',self.im1.sum())
        self._program['s_texture'] = gloo.Texture2D(self.im1)

        print(self.data)
        print(self.ensemble.sum())

        self._program.bind(gloo.VertexBuffer(self.data))

        # Set time to zero
        self._starttime = time.time()

    def set_data(self,ens_n):
        if ens_n!=-1:
            self.ensemble=self.U[:,ens_n]
        else:
            self.ensemble=np.ones(N,)
        #print(self.ensemble.sum())


from PyQt5.QtWidgets import *
import vispy.app
import sys

class MainWindow(QMainWindow):
    def __init__(self, canvas=None,parent=None):
        super(MainWindow, self).__init__(parent)
        self.canvas=canvas
        widget = QWidget()
        self.setCentralWidget(widget)
        self.l0 = QGridLayout()
        self.l0.addWidget(canvas.native)
        widget.setLayout(self.l0)

        self.n_ens=QLineEdit()
        self.n_ens.setText("0")
        self.n_ens.setFixedWidth(35)
        self.l0.addWidget(self.n_ens, 0, 4.5, 1, 2)
        self.n_ens.returnPressed.connect(lambda: self.on_set_n_ens())
        self.n_components=int(self.n_ens.text())

        self.update_view()


    def on_set_n_ens(self):
        self.n_components=int(self.n_ens.text())
        print('n_components',self.n_components)
        #self.show()
        self.update_view()

    def update_view(self):
        global i
        print(i)
        i=0
        self._starttime = time.time()
        self.canvas.set_data(self.n_components)
