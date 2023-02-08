package lab1


fun main(args: Array<String>) {
    val data = arrayListOf<Int>()
    repeat(10_000_000) {
        data.add(it)
    }
    logFunctionStats {
        BinarySearch(data).findElement(5)
    }
    logFunctionStats {
        BinarySearchMemoryOptimization(data).findElement(5)
    }
}

private fun logFunctionStats(func: () -> Unit) {
    val begin = System.nanoTime()
    func.invoke()
    val end = System.nanoTime()
    println("Time work (ms) : ${(end - begin) / 1e6}")
}
