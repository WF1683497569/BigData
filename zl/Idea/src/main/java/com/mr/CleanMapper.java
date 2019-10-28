package com.mr;

import com.alibaba.fastjson.JSONObject;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by 16834 on 2019/10/26.
 */
public class CleanMapper extends Mapper<LongWritable, Text, NullWritable, Text> {

    @Override
    protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

        //获取JSON的一行数据
        String rawJson = value.toString();
        //System.out.println("rawJson = " + rawJson);
        //解析JSON对象
        JSONObject jsonObject = JSONObject.parseObject(rawJson);
        //从JSON对象中获取相应信息
        String jobName = jsonObject.getString("jobName");
        String company = jsonObject.getString("company");
        String city = jsonObject.getString("city");
        String number = jsonObject.getString("number");
        String salary = jsonObject.getString("salary");
        String workingExp = jsonObject.getString("workingExp");

        //将符合条件的数据打包
        String[] datas = new String[6];
        datas[0] = jobName;
        datas[1] = company;
        datas[2] = city;
        datas[3] = number;
        datas[4] = salary;
        datas[5] = workingExp;

        //打包成一行数据
        StringBuilder result = new StringBuilder();
        for (String str : datas) {
            //将一行中的不同信息用竖线分割
            result.append(str).append("|");
        }
        if (result.length() > 1) {
            //删去最后一个竖线
            result.delete(result.length() - 1, result.length());
        }

        //写入Reduce任务
        context.write(NullWritable.get(), new Text(result.toString()));

    }
}
