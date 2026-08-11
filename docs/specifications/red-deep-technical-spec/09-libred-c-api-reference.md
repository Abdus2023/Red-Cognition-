# XVIII. LibRed C API — Complete Function Reference

```c
/* LIFECYCLE */
void  redOpen();
void  redClose();

/* EVALUATION */
RedValue redDo(const char* src);
RedValue redDoFile(char* path);
RedValue redDoBlock(RedValue blk);
RedValue redCall(const char* fn, ...);
RedValue redCallRef(RedValue fn, ...);

/* WORD ACCESS */
long     redSymbol(const char* word);
RedValue redGet(const char* word);
RedValue redSet(long sym, RedValue v);

/* DATATYPE CONSTRUCTORS */
RedValue redNone();
RedValue redLogic(int32_t logic);
RedValue redInteger(int32_t n);
RedValue redFloat(double f);
RedValue redString(const char* str);
RedValue redWord(const char* word);
RedValue redBlock(RedValue v, ...);
RedValue redPath(RedValue v, ...);

/* TYPE PREDICATES */
int32_t redTypeOf(RedValue v);
int32_t redIsNone(RedValue v);
int32_t redIsLogic(RedValue v);
int32_t redIsInteger(RedValue v);
int32_t redIsString(RedValue v);
int32_t redIsBlock(RedValue v);

/* VALUE EXTRACTION */
int32_t redCInt32(RedValue v);
double  redCDouble(RedValue v);
char*   redCString(RedValue v);

/* SERIES OPERATIONS */
RedValue redAppend(RedValue series, RedValue v);
RedValue redLength(RedValue series);
RedValue redIndex(RedValue series);
RedValue redHead(RedValue series);
RedValue redTail(RedValue series);
RedValue redNext(RedValue series);
RedValue redBack(RedValue series);
RedValue redPick(RedValue series, uint32_t index);
RedValue redPoke(RedValue series, uint32_t index, RedValue v);

/* PATH OPERATIONS */
RedValue redGetPath(RedValue root, ...);
RedValue redSetPath(RedValue v, ...);

/* CALLBACKS — Red calling C */
RedValue redRoutine(RedValue spec, const char* fn_name);

/* ERROR HANDLING */
int32_t redError(RedValue err);
void    redProbe(RedValue v);
void    redPrint(RedValue v);

/* CONSOLE/DEBUG */
void    redTraceback();
```