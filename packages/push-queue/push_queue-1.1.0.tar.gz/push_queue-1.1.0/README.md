#                         CustomQueue 

- CustomeQueue 继承自queue.Queue
- 只是新增一个push方法
  - push(new_item)
  - 当该队列满的时候,会将队列中最先入队列的元素old_item取出来,会将new_item放入队列
  - 然后返回old_item
  - 当队列不满的时候,直接将new_item入队列,然后返回None
  - 理论上这个方法不阻塞,也不会抛出异常