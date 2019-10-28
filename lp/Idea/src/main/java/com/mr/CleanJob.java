package com.mr;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;

/**
 * Created by 16834 on 2019/10/26.
 */

/**
 * 编写一个MR任务，清洗猎聘网Java工作岗位在特定城市的数据
 */
public class CleanJob {

    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {

        //初始化MR驱动
        Configuration conf = new Configuration();

        Job job = Job.getInstance(conf);
        job.setJarByClass(CleanJob.class);
        job.setMapperClass(CleanMapper.class);
        job.setReducerClass(CleanReducer.class);

        //设置Map输出
        job.setMapOutputKeyClass(NullWritable.class);
        job.setMapOutputValueClass(Text.class);

        //设置Reduce类型
        job.setOutputKeyClass(NullWritable.class);
        job.setOutputValueClass(Text.class);

        //设置输入输出路径
        FileInputFormat.addInputPath(job, new Path("E:/lp.json"));
        FileOutputFormat.setOutputPath(job, new Path("E:/result"));

        //在CleanJob任务完成后退出程序
        System.exit(job.waitForCompletion(true)?0:1);

    }

}
