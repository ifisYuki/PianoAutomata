using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Jump2Page2 : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void Jump() {
        SceneManager.LoadScene(1);
    }

    public void Back() {
        SceneManager.LoadScene(0);
    }
}
