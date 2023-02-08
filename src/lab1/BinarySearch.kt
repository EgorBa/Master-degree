package lab1

class BinarySearch<T : Comparable<T>>(private val data: List<T>) {

    fun findElement(element: T, fromIndex: Int = 0, toIndex: Int = data.size - 1): Int {
        return if (data.isEmpty() || toIndex < fromIndex) {
            -1
        } else {
            val pos = (fromIndex + toIndex) / 2
            when {
                data[pos] > element -> findElement(element, fromIndex, pos - 1)
                data[pos] < element -> findElement(element, pos + 1, toIndex)
                else -> pos
            }
        }
    }

}