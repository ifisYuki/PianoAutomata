/* SimpleMessageReceiver.cs */

using System;
using UnityEngine;

namespace extOSC.Examples
{
	[Serializable]
	public class MessageStartResponse  //用于握手协议的数据
	{
		public int error;
		public string message;
		public string clientid;
		public string token;
		public int timestamp;
	}

	[Serializable]
	public class MessageCommandResponse  //用于握手协议的数据
	{
		public int error;
		public string message;
		public int timestamp;
	}
	[Serializable]
	public class MessageSensorMessage  //用于握手协议的数据
	{
		public int sensor;//传感器编号
		public string [] value;
		public string serverid;
		public int timestamp;
	}

	public class SimpleMessageReceiver : MonoBehaviour
	{
		#region Public Vars

		public string Address = "/jsonmsg";

		[Header("OSC Settings")]
		public OSCReceiver Receiver;

		#endregion

		public SimpleMessageTransmitter transmitter;

		public int responseStatus;

		#region Unity Methods

		protected virtual void Start()
		{
			Receiver.Bind(Address, ReceivedMessage);
			responseStatus = 0;
		}

		#endregion

		#region Private Methods

		private void ReceivedMessage(OSCMessage message)
		{
			Debug.LogFormat("Received String: {0}", message.Values[0].StringValue);
			switch (responseStatus) {
				case 0:
					MessageStartResponse msp = JsonUtility.FromJson<MessageStartResponse>(message.Values[0].StringValue);
					if (msp.error == 0) {
						transmitter.token = msp.token;
						Debug.LogFormat("Respose JOSN: {0}", JsonUtility.ToJson(msp, true));
					}
					else
						Debug.LogFormat("Response Error: {0}", msp.message);
					break;
				case 10:
				case 1:
					MessageCommandResponse mcp = JsonUtility.FromJson<MessageCommandResponse>(message.Values[0].StringValue);
					if (mcp.error == 0) {
						//run successfully
						if (responseStatus == 10) {
							responseStatus = 100;//等待传感器数据
						}
					}
					break;
				case 100:
					MessageSensorMessage msm = JsonUtility.FromJson<MessageSensorMessage>(message.Values[0].StringValue);
					// 处理传感器数据
					break;
				default:
					Debug.LogFormat("Response Error: {0}", message.Values[0].StringValue);
					break;
			}
		}

		#endregion
	}
}