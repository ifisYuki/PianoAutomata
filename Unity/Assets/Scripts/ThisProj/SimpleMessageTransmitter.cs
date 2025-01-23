/* SimpleMessageTransmitter.cs */

using System;
using UnityEngine;

namespace extOSC.Examples
{
	//处理JSON数据，使用JsonUtility, 参考了 https://www.cnblogs.com/AdvancePikachu/p/7146731.html

	[Serializable]
	public class MessageStart  //用于握手协议的数据
	{
		public string command;
		public string id;
		public string server;
		public int timestamp;
	}

	[Serializable]
	public class MessageCommandSetting  //用于命令的设置项
	{
		public int node; //节点号
		public int power;//运行状态，可为0、1、2
		public int order;//运行顺序，第几个运行, 可多个同时运行，值范围 0 －15
		public int duration;//运行时长，可为0－循环不停，1－1秒，2，3
		public int delay;//完成后等待秒数
	}

	[Serializable]
	public class MessageCommand  //用于命令的数据
	{
		public string command;
		public string token;
		public string mode;
		public MessageCommandSetting [] settings;
		public int timestamp;
	}

	[Serializable]
	public class KeyNumber  //用于命令的数据
	{
		public string command;
		public string token;
		public string key_num;
		public MessageCommandSetting [] settings;
		public int timestamp;
	}

	public class SimpleMessageTransmitter : MonoBehaviour
	{
		#region Public Vars

		public string Address = "/jsonmsg";

		[Header("OSC Settings")]
		public OSCTransmitter Transmitter;
		#endregion


		public SimpleMessageReceiver receiver;

		protected static int timestampcount = 0;
		public string token;
		protected string ui_id = "yuki";
		protected string server = "pi";
		

		#region Unity Methods

		protected virtual void Start()
		{

			MessageStart ms = new MessageStart();
			ms.command = "conn"; //握手
			ms.id = this.ui_id;//UI编号
			ms.server = this.server; //要连接的服务器名字
			ms.timestamp = timestampcount ++;

			string json = JsonUtility.ToJson(ms, true);

			var message = new OSCMessage(Address);
			message.AddValue(OSCValue.String(json));

			Transmitter.Send(message);
		}

		#endregion

		#region Unity Methods

		public void RunPredefinedMode(string mode) // mode : 1, 2, ...
		{

			MessageCommand mc = new MessageCommand();
			mc.command = "run"; //
			mc.token = this.token;
			mc.mode = mode;
			mc.timestamp = timestampcount ++;

			string json = JsonUtility.ToJson(mc, true);

			var message = new OSCMessage(Address);
			message.AddValue(OSCValue.String(json));

			receiver.responseStatus = 1;
			Transmitter.Send(message);
		}

		#endregion

		#region Unity Methods

		public void RunDefaultMode(string mode) // mode : default_start, default_stop
		{

			MessageCommand mc = new MessageCommand();
			mc.command = "default"; //
			mc.token = this.token;
			mc.mode = mode;
			mc.timestamp = timestampcount ++;

			string json = JsonUtility.ToJson(mc, true);

			var message = new OSCMessage(Address);
			message.AddValue(OSCValue.String(json));

			receiver.responseStatus = 1;
			Transmitter.Send(message);
		}

		#endregion

		#region Unity Methods

		public void StopPredefinedMode(string mode) // mode : 1, 2, ...
		{

			MessageCommand mc = new MessageCommand();
			mc.command = "stop"; 
			mc.token = this.token;
			mc.mode = mode;
			mc.timestamp = timestampcount ++;

			string json = JsonUtility.ToJson(mc, true);

			var message = new OSCMessage(Address);
			message.AddValue(OSCValue.String(json));

			receiver.responseStatus = 1;
			Transmitter.Send(message);
		}

		#endregion

		#region Unity Methods

		public void RunCustomMode() //
		{

			MessageCommand mc = new MessageCommand();
			mc.command = "run"; //
			mc.token = this.token;
			mc.mode = "custom";
			//以下内容按需修改
			mc.settings = new MessageCommandSetting[10];
			for (int i = 0; i < 10; i ++) {
				mc.settings[i] = new MessageCommandSetting();
				mc.settings[i].node = i;
				mc.settings[i].power = 1;
				mc.settings[i].order = 2;
				mc.settings[i].duration = 5;
				mc.settings[i].delay = 0;
			}
			mc.timestamp = timestampcount ++;

			string json = JsonUtility.ToJson(mc, true);

			var message = new OSCMessage(Address);
			message.AddValue(OSCValue.String(json));

			receiver.responseStatus = 1;
			Transmitter.Send(message);
		}

		#endregion

		#region Unity Methods

		public void ChooseKeyNumber(string key_num)
		{

			KeyNumber kn = new KeyNumber();
			kn.command = "custom";
			kn.token = this.token;
			kn.key_num = key_num;
			kn.timestamp = timestampcount ++;

			string json = JsonUtility.ToJson(kn, true);

			var message = new OSCMessage(Address);
			message.AddValue(OSCValue.String(json));

			receiver.responseStatus = 1;
			Transmitter.Send(message);
		}

		#endregion
	}
}