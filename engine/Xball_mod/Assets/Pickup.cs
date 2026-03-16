using UnityEngine;

public class Pickup : MonoBehaviour
{
    public Material material;

    float time = 0.0f;
    float thresh = 1.0f;
    float height = 1.0f;
    Color color;
    Vector3 pos;
    Vector2 lim;
    Vector3 scale;
    GameObject go;
    Renderer rend;

    void Start()
    {
        lim.x = 15.0f;
        lim.y = 10.0f;
        scale.x = 0.25f;
        scale.y = 0.25f;
        scale.z = 0.25f;
    }

    void Update()
    {
        time += Time.deltaTime;
        if (time > thresh)
        {
            Create();
            time = 0.0f;
        }
    }

    void Create()
    {
        color = new Color(Random.Range(-0.5f, 0.5f),
                          Random.Range(-0.5f, 0.5f),
                          Random.Range(-0.5f, 0.5f), 0.5f);
        pos = new Vector3(Random.Range(-0.5f, 0.5f) * lim.x, height,
                          Random.Range(-0.5f, 0.5f) * lim.y);
        go = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        go.transform.localScale = scale;
        go.transform.position = pos;
        rend = go.GetComponent<Renderer>();
        rend.material = material;
        go.GetComponent<Renderer>().material.SetVector("_Chroma", color);
        go.AddComponent<Particle>();
        go.GetComponent<Particle>().attract = transform;
        go.GetComponent<Particle>().audio_src = this.GetComponent<AudioSource>();
    }
}
