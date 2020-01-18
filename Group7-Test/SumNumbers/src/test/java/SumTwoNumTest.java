import static org.hamcrest.CoreMatchers.instanceOf;
import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.List;

import org.junit.Test;
public class SumTwoNumTest {

    @Test
    public void test1(){
        int expected = 5;
        int actual = SumTwoNum.sumTwoNum(2 , 3);
        assertEquals(expected, actual);
    }

    @Test
    public void test2(){
        int expected = 4;
        int actual = SumTwoNum.sumTwoNum(2 , 2);
        assertEquals(expected, actual);
    }

}
