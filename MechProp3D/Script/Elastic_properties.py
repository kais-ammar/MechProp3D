#########################################################################################################################
#############ELATE: Elastic tensor analysis##############################################################################
########J. Phys. Condens. Matter, 2016, 28, 275201#######################################################################
######### This script is developed by Romain Gaillac and François-Xavier Coudert at CNRS / Chimie ParisTech.#############
#########################################################################################################################

import math
import numpy as np
import numpy.linalg as la
from scipy import optimize

def write3DPlotData_vtk(name, dataX, dataY, dataZ, dataR):
   ###########write_vtk_grid_values_3D###############
  #-- open output file
  out = open(name+'.vtk','w')
  # start writing ASCII VTK file:
  # header of VTK file
  string  = '# vtk DataFile Version 2.0\n'
  string  += 'output.vtk\n'
  string  += 'ASCII\n'
  string  += 'DATASET STRUCTURED_GRID\n'
  #--- coords of grid points:
  string  += 'DIMENSIONS %5d %5d %5d\n'%(len(dataX[0]),len(dataX),1)
  string  += 'POINTS %7d float\n'%(np.size(dataX))
  for cu in range(len(dataX)):
    for cv in range(len(dataX[0])):  
       string  +=  '%14.6e %14.6e %14.6e\n'%(dataX[cu][cv],dataY[cu][cv],dataZ[cu][cv])
  #--- write grid point values:
  string  +='POINT_DATA %5d\n' %(np.size(dataX))
  string  +='SCALARS VARIABLE float 1 \n'
  string  +='LOOKUP_TABLE default\n'
  for cu in range(len(dataX)):
    for cv in range(len(dataX[0])):  
       string  +=  '%14.6e\n'%(dataR[cu][cv])
  out.write(string)
  out.close() 
  
def GENERATE_PLOT3D(matrix, type):
  elas = Elastic(matrix)
  if elas.isOrthorhombic():
    elas = ElasticOrtho(elas)
    
  if type == "young" : 
    dataX, dataY, dataZ, dataR = YOUNG_3D(lambda x,y: elas.Young3D(x,y), "Young's modulus in 3D")       
  elif  type == "shear" :
    dataX, dataY, dataZ, dataR = SHEAR_3D(lambda x,y,g1,g2: elas.shear3D(x,y,g1,g2), "Shear modulus in 3D")
  elif  type == "poisson" :
    dataX, dataY, dataZ, dataR = POISSON_3D(lambda x,y,g1,g2: elas.poisson3D(x,y,g1,g2), "Poisson's ratio in 3D")
  elif  type == "compressiblity" :
    dataX, dataY, dataZ, dataR = Bulk_3D(lambda x,y: elas.LC3D(x,y), "Linear compressiblity in 3D")     
  else :
      raise ValueError('ERRROR')
  return dataX, dataY, dataZ, dataR   
  
def YOUNG_3D(func, legend, npoints = 50):
  u = np.linspace(0, np.pi, npoints)
  v = np.linspace(0, 2*np.pi, 2*npoints)
  dataX = np.zeros((len(u),len(v)))
  dataY = np.zeros((len(u),len(v)))
  dataZ = np.zeros((len(u),len(v)))
  dataR = np.zeros((len(u),len(v)))

  for cu in range(len(u)):
    for cv in range(len(v)):
      r_tmp = func(u[cu],v[cv])
      z = r_tmp * np.cos(u[cu])
      x = r_tmp * np.sin(u[cu]) * np.cos(v[cv])
      y = r_tmp * np.sin(u[cu]) * np.sin(v[cv])
      dataX[cu][cv] = x
      dataY[cu][cv] = y
      dataZ[cu][cv] = z
      dataR[cu][cv] = r_tmp
  return dataX, dataY, dataZ, dataR

def SHEAR_3D(func, legend, npoints = 50):

  u = np.linspace(0, np.pi, npoints)
  v = np.linspace(0, np.pi, npoints)
  w = [v[i]+np.pi for i in range(1,len(v))]
  v = np.append(v, w)

  dataX1 = np.zeros((len(u),len(v)))
  dataY1 = np.zeros((len(u),len(v)))
  dataZ1 = np.zeros((len(u),len(v)))
  dataR1 = np.zeros((len(u),len(v)))
  
  dataX2 = np.zeros((len(u),len(v)))
  dataY2 = np.zeros((len(u),len(v)))
  dataZ2 = np.zeros((len(u),len(v)))
  dataR2 = np.zeros((len(u),len(v)))

  r = [0.0,0.0,np.pi/2.0,np.pi/2.0]
  for cu in range(len(u)):
    for cv in range(len(v)):

      r = func(u[cu],v[cv],r[2],r[3])
      z = np.cos(u[cu])
      x = np.sin(u[cu]) * np.cos(v[cv])
      y = np.sin(u[cu]) * np.sin(v[cv])

      r1_tmp = r[0]
      z1 = r1_tmp * z
      x1 = r1_tmp * x
      y1 = r1_tmp * y
      dataX1[cu][cv] = x1
      dataY1[cu][cv] = y1
      dataZ1[cu][cv] = z1
      dataR1[cu][cv] = r1_tmp

      r2_tmp = r[1]
      z2 = r2_tmp * z
      x2 = r2_tmp * x
      y2 = r2_tmp * y
      dataX2[cu][cv] = x2
      dataY2[cu][cv] = y2
      dataZ2[cu][cv] = z2
      dataR2[cu][cv] = r2_tmp    
  dataX = np.concatenate((dataX1, dataX2), axis=0)
  dataY = np.concatenate((dataY1, dataY2), axis=0)
  dataZ = np.concatenate((dataZ1, dataZ2), axis=0)
  dataR = np.concatenate((dataR1, dataR2), axis=0)
  return dataX, dataY, dataZ, dataR
  

def POISSON_3D(func, legend, npoints = 50):
  u = np.linspace(0, np.pi, npoints)
  v = np.linspace(0, np.pi, npoints)
  w = [v[i]+np.pi for i in range(1,len(v))]
  v = np.append(v, w)

  dataX1 = np.zeros((len(u),len(v)))
  dataY1 = np.zeros((len(u),len(v)))
  dataZ1 = np.zeros((len(u),len(v)))
  dataR1 = np.zeros((len(u),len(v)))
  
  dataX2 = np.zeros((len(u),len(v)))
  dataY2 = np.zeros((len(u),len(v)))
  dataZ2 = np.zeros((len(u),len(v)))
  dataR2 = np.zeros((len(u),len(v)))

  dataX3 = np.zeros((len(u),len(v)))
  dataY3 = np.zeros((len(u),len(v)))
  dataZ3 = np.zeros((len(u),len(v)))
  dataR3 = np.zeros((len(u),len(v)))  
  
  r = [0.0, 0.0, 0.0, np.pi/2.0, np.pi/2.0]
  ruv = [[r for i in range(len(u))] for j in range(len(v))]
  for cu in range(len(u)):
    for cv in range(len(v)):
       ruv[cv][cu] = func(u[cu],v[cv],r[3],r[4])

  for cu in range(len(u)):
    for cv in range(len(v)):
      z = np.cos(u[cu])
      x = np.sin(u[cu]) * np.cos(v[cv])
      y = np.sin(u[cu]) * np.sin(v[cv])

      r = ruv[cv][cu]
      dataX1[cu][cv] = r[0] * x
      dataY1[cu][cv] = r[0] * y
      dataZ1[cu][cv] = r[0] * z
      dataR1[cu][cv] = r[0]

      dataX2[cu][cv] = r[1] * x
      dataY2[cu][cv] = r[1] * y
      dataZ2[cu][cv] = r[1] * z
      dataR2[cu][cv] = r[1]
      
      dataX3[cu][cv] = r[2] * x
      dataY3[cu][cv] = r[2] * y
      dataZ3[cu][cv] = r[2] * z
      dataR3[cu][cv] = r[2]

  dataX = np.concatenate((dataX1, dataX2, dataX3), axis=0)
  dataY = np.concatenate((dataY1, dataY2, dataY3), axis=0)
  dataZ = np.concatenate((dataZ1, dataZ2, dataZ3), axis=0)
  dataR = np.concatenate((dataR1, dataR2, dataR3), axis=0)
  return dataX, dataY, dataZ, dataR

def Bulk_3D(func, legend, npoints = 50):
  u = np.linspace(0, np.pi, npoints)
  v = np.linspace(0, 2*np.pi, 2*npoints)  
  dataX = np.zeros((len(u),len(v)))
  dataY = np.zeros((len(u),len(v)))
  dataZ = np.zeros((len(u),len(v)))
  dataR = np.zeros((len(u),len(v)))
  
  for cu in range(len(u)):
    for cv in range(len(v)):
      r_tmp = max(0,func(u[cu],v[cv]))
      z = r_tmp * np.cos(u[cu])
      x = r_tmp * np.sin(u[cu]) * np.cos(v[cv])
      y = r_tmp * np.sin(u[cu]) * np.sin(v[cv])
      dataX[cu][cv] = x
      dataY[cu][cv] = y
      dataZ[cu][cv] = z
      dataR[cu][cv] = r_tmp
  return dataX, dataY, dataZ, dataR

def dirVec(theta, phi):
  return [ math.sin(theta)*math.cos(phi), math.sin(theta)*math.sin(phi), math.cos(theta) ]


def dirVec2(theta, phi, chi):
  return [ math.cos(theta)*math.cos(phi)*math.cos(chi) - math.sin(phi)*math.sin(chi),
          math.cos(theta)*math.sin(phi)*math.cos(chi) + math.cos(phi)*math.sin(chi),
          - math.sin(theta)*math.cos(chi) ]

# Functions to minimize/maximize
def minimize(func, dim):
  if dim == 2:
    r = ((0, np.pi), (0, np.pi))
    n = 25
  elif dim == 3:
    r = ((0, np.pi), (0, np.pi), (0, np.pi))
    n = 10
  return optimize.brute(func, r, Ns = n, full_output = True, finish = optimize.fmin)[0:2]

class Elastic:
  def __init__(self, s):
    """Initialize the elastic tensor from a string"""
    mat = s
    if mat.shape != (6,6):
      # Is it upper triangular?
      if list(map(len, mat)) == [6,5,4,3,2,1]:
        mat = [ [0]*i + mat[i] for i in range(6) ]
        mat = np.array(mat)

      # Is it lower triangular?
      if list(map(len, mat)) == [1,2,3,4,5,6]:
        mat = [ mat[i] + [0]*(5-i) for i in range(6) ]
        mat = np.array(mat)

    if mat.shape != (6,6):
      raise ValueError("should be a square matrix")

    # Check that is is symmetric, or make it symmetric
    if la.norm(np.tril(mat, -1)) == 0:
      mat = mat + np.triu(mat, 1).transpose()
    if la.norm(np.triu(mat, 1)) == 0:
      mat = mat + np.tril(mat, -1).transpose()
    if la.norm(mat - mat.transpose()) > 1e-3:
      raise ValueError("should be symmetric, or triangular")
    elif la.norm(mat - mat.transpose()) > 0:
      mat = 0.5 * (mat + mat.transpose())

    # Store it
    self.CVoigt = mat
    try:
      self.SVoigt = la.inv(self.CVoigt)
    except:
      raise ValueError("matrix is singular")
   
    VoigtMat = [[0, 5, 4], [5, 1, 3], [4, 3, 2]]
    def SVoigtCoeff(p,q): return 1. / ((1+p//3)*(1+q//3))

    self.Smat = [[[[ SVoigtCoeff(VoigtMat[i][j], VoigtMat[k][l]) * self.SVoigt[VoigtMat[i][j]][VoigtMat[k][l]]
                     for i in range(3) ] for j in range(3) ] for k in range(3) ] for l in range(3) ]
    return

  def isOrthorhombic(self):
    def iszero(x): return (abs(x) < 1.e-3)
    return (iszero(self.CVoigt[0][3]) and iszero(self.CVoigt[0][4]) and iszero(self.CVoigt[0][5])
            and iszero(self.CVoigt[1][3]) and iszero(self.CVoigt[1][4]) and iszero(self.CVoigt[1][5])
            and iszero(self.CVoigt[2][3]) and iszero(self.CVoigt[2][4]) and iszero(self.CVoigt[2][5])
            and iszero(self.CVoigt[3][4]) and iszero(self.CVoigt[3][5]) and iszero(self.CVoigt[4][5]))

  def Young3D(self,x,y):
    a = dirVec(x, y)
    r = sum([ a[i]*a[j]*a[k]*a[l] * self.Smat[i][j][k][l]
              for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
    return 1/r

  def shear(self, x):
    a = dirVec(x[0], x[1])
    b = dirVec2(x[0], x[1], x[2])
    r = sum([ a[i]*b[j]*a[k]*b[l] * self.Smat[i][j][k][l]
              for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
    return 1/(4*r)

  def Poisson(self, x):
    a = dirVec(x[0], x[1])
    b = dirVec2(x[0], x[1], x[2])
    r1 = sum([ a[i]*a[j]*b[k]*b[l] * self.Smat[i][j][k][l]
              for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
    r2 = sum([ a[i]*a[j]*a[k]*a[l] * self.Smat[i][j][k][l]
              for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
    return -r1/r2

  def LC3D(self, x, y):
    a = dirVec(x, y)
    r = sum([ a[i]*a[j] * self.Smat[i][j][k][k]
              for i in range(3) for j in range(3) for k in range(3)])
    return 1000 * r

  def shear3D(self, x, y, guess1 = np.pi/2.0, guess2 = np.pi/2.0):
    tol = 0.005
    def func1(z): return self.shear([x, y, z])
    r1 = optimize.minimize(func1, guess1, args=(), method = 'COBYLA', options={"tol":tol})#, bounds=[(0.0,np.pi)])
    def func2(z): return -self.shear([x, y, z])
    r2 = optimize.minimize(func2, guess2, args=(), method = 'COBYLA', options={"tol":tol})#, bounds=[(0.0,np.pi)])
    return (float(r1.fun), -float(r2.fun), float(r1.x), float(r2.x))

  def poisson3D(self, x, y, guess1 = np.pi/2.0, guess2 = np.pi/2.0):
    tol = 0.005
    def func1(z): return self.Poisson([x, y, z])
    r1 = optimize.minimize(func1, guess1, args=(), method = 'COBYLA', options={"tol":tol})#, bounds=[(0.0,np.pi)])
    def func2(z): return -self.Poisson([x, y, z])
    r2 = optimize.minimize(func2, guess2, args=(), method = 'COBYLA', options={"tol":tol})#, bounds=[(0.0,np.pi)])
    return (min(0,float(r1.fun)), max(0,float(r1.fun)), -float(r2.fun), float(r1.x), float(r2.x))

class ElasticOrtho(Elastic):
  """An elastic tensor, for the specific case of an orthorhombic system"""
  def __init__(self, arg):
    """Initialize from a matrix, or from an Elastic object"""
    self.CVoigt = arg.CVoigt
    self.SVoigt = arg.SVoigt
    self.Smat = arg.Smat
    
  def shear(self, x):
    ct = math.cos(x[0])
    ct2 = ct*ct
    st2 = 1 - ct2
    cf = math.cos(x[1])
    sf = math.sin(x[1])
    sf2 = sf*sf
    cx = math.cos(x[2])
    cx2 = cx*cx
    sx = math.sin(x[2])
    sx2 = 1 - cx2
    s11 = self.Smat[0][0][0][0]
    s22 = self.Smat[1][1][1][1]
    s33 = self.Smat[2][2][2][2]
    s44 = 4 * self.Smat[1][2][1][2]
    s55 = 4 * self.Smat[0][2][0][2]
    s66 = 4 * self.Smat[0][1][0][1]
    s12 = self.Smat[0][0][1][1]
    s13 = self.Smat[0][0][2][2]
    s23 = self.Smat[1][1][2][2]
    r = ( ct2*ct2*cx2*s44*sf2 + cx2*s44*sf2*st2*st2 + 4*cf**3*ct*cx*(-2*s11 + 2*s12 + s66)*sf*st2*sx
          + 2*cf*ct*cx*sf*(ct2*(s44 - s55) + (4*s13 - 4*s23 - s44 + s55 - 4*s12*sf2 + 4*s22*sf2 - 2*s66*sf2)*st2)*sx
          + s66*sf2*sf2*st2*sx2 + cf**4*st2*(4*ct2*cx2*s11 + s66*sx2)
          + ct2*(2*cx2*(2*s33 + sf2*(-4*s23 - s44 + 2*s22*sf2))*st2 + s55*sf2*sx2)
          + cf**2*(ct2*ct2*cx2*s55 + ct2*(-2*cx2*(4*s13 + s55 - 2*(2*s12 + s66)*sf2)*st2 + s44*sx2)
                   + st2*(cx2*s55*st2 + 2*(2*s11 - 4*s12 + 2*s22 - s66)*sf2*sx2))
        )
    return 1/r

  def Poisson(self, x):
    ct = math.cos(x[0])
    ct2 = ct*ct
    st2 = 1 - ct2
    cf = math.cos(x[1])
    sf = math.sin(x[1])
    cx = math.cos(x[2])
    sx = math.sin(x[2])
    s11 = self.Smat[0][0][0][0]
    s22 = self.Smat[1][1][1][1]
    s33 = self.Smat[2][2][2][2]
    s44 = 4 * self.Smat[1][2][1][2]
    s55 = 4 * self.Smat[0][2][0][2]
    s66 = 4 * self.Smat[0][1][0][1]
    s12 = self.Smat[0][0][1][1]
    s13 = self.Smat[0][0][2][2]
    s23 = self.Smat[1][1][2][2]

    return ((-(ct**2*cx**2*s33*st2) - cf**2*cx**2*s13*st2*st2 - cx**2*s23*sf**2*st2*st2 + ct*cx*s44*sf*st2*(ct*cx*sf + cf*sx) -
          ct**2*s23*(ct*cx*sf + cf*sx)**2 - cf**2*s12*st2*(ct*cx*sf + cf*sx)**2 - s22*sf**2*st2*(ct*cx*sf + cf*sx)**2 +
          cf*ct*cx*s55*st2*(cf*ct*cx - sf*sx) - cf*s66*sf*st2*(ct*cx*sf + cf*sx)*(cf*ct*cx - sf*sx) -
          ct**2*s13*(cf*ct*cx - sf*sx)**2 - cf**2*s11*st2*(cf*ct*cx - sf*sx)**2 - s12*sf**2*st2*(cf*ct*cx - sf*sx)**2)/
        (ct**4*s33 + 2*cf**2*ct**2*s13*st2 + cf**2*ct**2*s55*st2 + 2*ct**2*s23*sf**2*st2 + ct**2*s44*sf**2*st2 +
          cf**4*s11*st2*st2 + 2*cf**2*s12*sf**2*st2*st2 + cf**2*s66*sf**2*st2*st2 + s22*sf**4*st2*st2))

