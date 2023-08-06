#include <Python.h>
#include <time.h>
 
static PyObject* lfgToFile(PyObject* self, PyObject* args)
{
  const char* fname;
  unsigned int size;
  unsigned int i;
  unsigned int *ptr;
  int lag, seedsize;
  unsigned char k,j;    
  FILE *fd;
  unsigned int MODULUS;
  MODULUS = 0xFFFFFFFF;
  
  if (!PyArg_ParseTuple(args, "iiis", &size, &lag, &seedsize,&fname))
    return NULL;
  unsigned int seed[seedsize]; 
  fd = fopen(fname,"wb");
  
  j = lag;
  k = seedsize;
  srand ( time(NULL) );
  
  for (i=1; i <= seedsize ; i++)
    {  
      //seed[i] = rand() % (1024*1024*1024*2);
      seed[i] = rand()  ;
    }
  for (i=0; i < (size / sizeof(seed[0])); i++)
    {      
      //seed[k]= (seed[k] + seed[j]) % (1024*1024*1024*2);
      seed[k]= (seed[k] + seed[j]);
      ptr = &seed[k];
      fwrite(ptr, sizeof(seed[1]),1,fd);
      j -= 1;
      k -= 1;
      if (j == 0) j = seedsize;
      if (k == 0) k = seedsize;
    } 
  fclose(fd);  
  Py_RETURN_NONE;  
}

static PyObject* lfgToList(PyObject* self, PyObject* args)
{
  unsigned int size;
  unsigned int i;
  int lag, seedsize;
  unsigned char k,j;    

  if (!PyArg_ParseTuple(args, "iii", &size, &lag, &seedsize))
    return NULL;
  unsigned int seed[seedsize]; 
  PyObject* lst = PyList_New(size);  

  j = lag;
  k = seedsize;
  srand ( time(NULL) );
  
  for (i=1; i <= seedsize ; i++)
    {  
      seed[i] = rand() % (1024*1024*1024*2);
    }

  for (i=0; i < size; i++)
    {      
      seed[k]= (seed[k] + seed[j]) % (1024*1024*1024*2);
      PyList_SetItem(lst,i, Py_BuildValue("i",seed[k]));
      j -= 1;
      k -= 1;
      if (j == 0) j = seedsize;
      if (k == 0) k = seedsize;
    } 
  return lst;
}
 
static PyMethodDef rngMethods[] =
{
     {"lfgToFile", lfgToFile, METH_VARARGS, "lfgToFile(size, param1, param2, filename): This method will generate a file with the given parameters."},
     {"lfgToList", lfgToList, METH_VARARGS, "lfgToList(size, param1, param2): This method will return a list of numbers."},
     {NULL, NULL, 0, NULL}
};


static struct PyModuleDef rngmodule = {
  PyModuleDef_HEAD_INIT,
  "rnglfg",
  NULL, 
  -1,
  rngMethods

};

/* 
PyMODINIT_FUNC
 
initrng(void)
{
     (void) Py_InitModule("rng", rngMethods);
}
*/


PyMODINIT_FUNC
PyInit_rnglfg(void)
{
  Py_Initialize();
  return PyModule_Create(&rngmodule);
}
