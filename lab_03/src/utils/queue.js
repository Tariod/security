class Queue {
  constructor(maxSize = 624) {
    this._maxSize = maxSize;
    this._size = 0;
    this._head = null;
    this._tail = null;
  }

  shift() {
    if (this._head) {
      if (this._head === this._tail) {
        this._tail = null;
      }
      this._head = this._head.next;
      this._size--;
    }

    return this;
  }

  push(value) {
    const node = { value, next: null };
    if (this._head === null) {
      this._head = node;
    }

    if (this._tail !== null) {
      this._tail.next = node;
    }

    this._tail = node;
    this._size++;

    if (this._size > this._maxSize) {
      this.shift();
    }

    return this;
  }

  toArray() {
    const arr = new Uint32Array(this._size);
    let temp = this._head;
    for (let i = 0; i < this._size; i++) {
      arr[i] = temp.value;
      temp = temp.next;
    }
    return arr;
  }
}

module.exports = Queue;
