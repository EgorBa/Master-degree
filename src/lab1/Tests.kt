package lab1

import org.junit.jupiter.api.Test
import kotlin.random.Random.Default.nextDouble
import kotlin.random.Random.Default.nextInt
import kotlin.test.assertEquals

class Tests {

    private class Checker<T : Comparable<T>> {
        fun check(data: List<T>) {
            for (element in data) {
                val result1 = BinarySearchMemoryOptimization(data).findElement(element)
                val result2 = BinarySearch(data).findElement(element)
                val expected = data.binarySearch(element)
                assertEquals(expected, result1)
                assertEquals(expected, result2)
            }
        }

        @Test
        fun stressTest(functionForGenerate: () -> T) {
            val testCount = 1000
            val listSize = 1000
            repeat(testCount) {
                val set = hashSetOf<T>()
                repeat(listSize) {
                    set.add(functionForGenerate.invoke())
                }
                check(set.toList().sorted())
            }
        }
    }

    @Test
    fun emptyData() {
        val data = emptyList<Int>()
        Checker<Int>().check(data)
    }

    @Test
    fun simpleTestWithOddElementsCount() {
        val data = listOf(1, 2, 3)
        Checker<Int>().check(data)
    }

    @Test
    fun simpleTestWithEvenElementsCount() {
        val data = listOf(1, 2, 3, 4)
        Checker<Int>().check(data)
    }

    @Test
    fun stressTestInt() {
        Checker<Int>().stressTest {
            nextInt(0, 1_000_000)
        }
    }

    @Test
    fun stressTestDouble() {
        Checker<Double>().stressTest {
            nextDouble(0.0, 1_000_000.0)
        }
    }

}