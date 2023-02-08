package lab1

class BinarySearchMemoryOptimization<T : Comparable<T>>(private val data: List<T>) {

    fun findElement(element: T, fromIndex: Int = 0, toIndex: Int = data.size - 1): Int {
        if (data.isEmpty() || toIndex < fromIndex) {
            return -1
        } else {
            var from = fromIndex
            var to = toIndex
            do {
                val pos = (from + to) / 2
                when {
                    data[pos] > element -> to = pos - 1
                    data[pos] < element -> from = pos + 1
                    data[pos] == element -> return pos
                }
            } while (to >= from)
            return -1
        }
    }

}