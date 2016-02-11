package com.example.marc.applicartel;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import java.util.HashMap;

import android.widget.ListAdapter;
import android.widget.SimpleAdapter;


public class FilActus extends AppCompatActivity implements NavigationView.OnNavigationItemSelectedListener {

    public final static String BLA = "bla";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.filactu_activity);

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);


        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);  //Menu apparaissant à gauche, trois traits
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        ListView vueListeActus = (ListView) findViewById(R.id.xlisteActus);

        final LinkedList<Actu> lact = new LinkedList<>();
        String texteActu;
        texteActu = "youpi\nwaza\nAlbi c'était vraiment des kikous\n#c'estnouslesmeilleurs\n#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur\n" +
                "#bushenkeur";
        lact.add(new Actu("Paris gagne !", 2, "25/04/2016", "17:49",getResources().getIdentifier("willrunforbeer", "drawable", getPackageName()) , "Willy Wonka", texteActu));
        texteActu = "on s'est cassé le cul mais ça a l'air de marcher\non verra bien";
        lact.add(new Actu("Lancement de l'application.",3 , "10/03/2016", "14:52", getResources().getIdentifier("willrunforbeer", "drawable", getPackageName()), "Marc", texteActu));


        List<HashMap<String, String>> liste = new ArrayList<HashMap<String, String>>();

        HashMap<String, String> element;
        for (int i = 0;i<lact.size();i++){
            element = new HashMap<String, String>();

            element.put("titre", lact.get(i).titre );

            element.put("date&heure", "Le "+lact.get(i).date+" à "+lact.get(i).heure+".");
            liste.add(element);
        }

        ListAdapter adapter = new SimpleAdapter(this, liste, android.R.layout.simple_list_item_2, new String[]{"titre","date&heure"}, new int[] {android.R.id.text1, android.R.id.text2 });
        vueListeActus.setAdapter(adapter);




        vueListeActus.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> adapterView,
                                    View view,
                                    int position,
                                    long id) {
                Intent iActuActiv = new Intent(FilActus.this, ActuActiv.class);
                iActuActiv.putExtra(FilActus.BLA, lact.get(position));
                // Puis on lance l'intent !
                startActivity(iActuActiv);
            }
        });


        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.accueil, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();

        if (id == R.id.accueil) {
            finish();
        } else if (id == R.id.filactu) {

        } else if (id == R.id.nav_gallery) {

        } else if (id == R.id.nav_slideshow) {

        } else if (id == R.id.nav_manage) {

        } else if (id == R.id.nav_share) {

        } else if (id == R.id.nav_send) {

        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
