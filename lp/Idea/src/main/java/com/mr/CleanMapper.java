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
        String name = jsonObject.getString("职位");
        String company = jsonObject.getString("公司");
        String salary = jsonObject.getString("薪资");
        String place = jsonObject.getString("地点");
        String study = jsonObject.getString("学历");
        String uri = jsonObject.getString("uri");

        //构建筛选条件，例如工作城市只在以下words数组中，如有，newRequire中有相关数据，没有则过滤此行JSON数据
        List<String> newRequire = new ArrayList<String>();
        String[] words = "北京、上海、武汉、深圳、天津、杭州、大连".split("、");
        //遍历words数组，如果包含地点place信息，则添加到newRequire中
        for (int i = 0; i < words.length; i++) {
            if (place.contains(words[i])) {
                newRequire.add(words[i]);
            }
        }
        //System.out.println("newRequire = " + newRequire.toString());

        //将符合条件的数据打包
        String[] datas = new String[6];
        if (newRequire.size() != 0) {
            datas[0] = name;
            datas[1] = company;
            datas[2] = salary;
            //处理数据newRequire = [杭州]，去掉方括号
            datas[3] = newRequire.toString().replace("[", "").replace("]", "");
            datas[4] = study;
            datas[5] = uri;

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
}
